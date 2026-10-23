import { CHURCH, SERVICES, FALLBACK_CATEGORY, CATEGORY_LABELS } from './layouts.js';

const CONFIG = window.SONGS_CONFIG || { emailjs: {} };
const STORE = { lineup: 'melody.lineup.v1', recipients: 'melody.recipients.v1', history: 'melody.history.v1', prefs: 'melody.prefs.v1' };
const EMAILJS_URL = 'https://api.emailjs.com/api/v1.0/email/send';

const $ = (sel, root = document) => root.querySelector(sel);
const el = (tag, props = {}, ...kids) => {
  const node = Object.assign(document.createElement(tag), props);
  for (const k of kids.flat()) if (k != null && k !== false) node.append(k);
  return node;
};

// ---------- storage ----------
function load(key, fallback) {
  try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch { return fallback; }
}
function save(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode: keep working in memory */ }
}

// ---------- songs ----------
const pools = {};      // category -> [song]
const allSongs = [];   // deduped across categories

function titleCase(s) {
  return s.toLowerCase().replace(/(^|[\s(\-"/])([a-z])/g, (_, a, b) => a + b.toUpperCase());
}

function parseCsv(text) {
  return text.split(/\r?\n/).map(l => l.trim()).filter(Boolean).map(line => {
    const parts = line.split(',').map(p => p.trim());
    const [title, number = '', verses = ''] = parts;
    const rest = parts.slice(3).filter(Boolean);
    return {
      title: titleCase(title),
      number,
      verses: verses.split(/\s+/).filter(Boolean).join(' '),
      chorus: rest[0] === '1',
      note: rest.filter(x => x !== '0' && x !== '1').join(', '),
    };
  });
}

async function loadSongs() {
  const cats = new Set([...Object.keys(CATEGORY_LABELS), ...SERVICES.flatMap(s => s.steps.filter(x => x.song).map(x => x.song))]);
  await Promise.all([...cats].map(async cat => {
    try {
      const res = await fetch(`songs/${cat}.csv`, { cache: 'no-cache' });
      pools[cat] = res.ok ? parseCsv(await res.text()) : [];
    } catch { pools[cat] = []; }
    pools[cat].forEach(s => (s.cat = cat));
  }));
  const seen = new Set();
  for (const cat of cats) for (const s of pools[cat]) {
    if (!seen.has(keyOf(s))) { seen.add(keyOf(s)); allSongs.push(s); }
  }
  allSongs.sort((a, b) => a.title.localeCompare(b.title));
}

const keyOf = s => (s.number || s.title || '').toLowerCase();
const copySong = s => s && { title: s.title, number: s.number, verses: s.verses, chorus: s.chorus, note: s.note || '' };

// ---------- dates ----------
const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const fromIso = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
function upcomingSunday() {
  const d = new Date();
  d.setDate(d.getDate() + ((7 - d.getDay()) % 7));
  return iso(d);
}
const longDate = s => fromIso(s).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

// ---------- state ----------
let prefs = { avoidWeeks: 4, emailjs: {}, ...load(STORE.prefs, {}) };
let recipients = load(STORE.recipients, []);
let history = load(STORE.history, {});   // sunday iso -> [song keys], sends from this device
let shared = { status: 'off', history: {} };   // same shape, from the shared Google Sheet
let state = load(STORE.lineup, null);

const persist = () => save(STORE.lineup, state);

function recentKeys() {
  const weeks = Number(prefs.avoidWeeks) || 0;
  if (!weeks) return new Set();
  const now = fromIso(state.sunday).getTime();
  const out = new Set();
  for (const [day, keys] of [...Object.entries(history), ...Object.entries(shared.history)]) {
    const age = (now - fromIso(day).getTime()) / 864e5;
    if (day !== state.sunday && age > 0 && age <= weeks * 7) keys.forEach(k => out.add(k));
  }
  return out;
}

function usedKeys(except) {
  const out = new Set();
  for (const svc of SERVICES) {
    const st = state.services[svc.id];
    if (!st.include) continue;
    st.slots.forEach((slot, i) => {
      if (slot.song && !(except && except.svc === svc.id && except.i === i)) out.add(keyOf(slot.song));
    });
  }
  return out;
}

function pick(cat, exclude) {
  const recent = recentKeys();
  const tries = [
    pools[cat]?.filter(s => !exclude.has(keyOf(s)) && !recent.has(keyOf(s))),
    pools[cat]?.filter(s => !exclude.has(keyOf(s))),
    pools[FALLBACK_CATEGORY]?.filter(s => !exclude.has(keyOf(s)) && !recent.has(keyOf(s))),
    pools[FALLBACK_CATEGORY]?.filter(s => !exclude.has(keyOf(s))),
  ];
  const list = tries.find(t => t && t.length);
  return list ? copySong(list[Math.floor(Math.random() * list.length)]) : null;
}

function rerollSlot(svcId, i) {
  const slot = state.services[svcId].slots[i];
  const exclude = usedKeys({ svc: svcId, i });
  if (slot.song) exclude.add(keyOf(slot.song));
  const song = pick(slot.cat, exclude);
  if (song) slot.song = song; else toast('No more songs left in that category');
}

function rerollService(svcId, { includeLocked = false } = {}) {
  state.services[svcId].slots.forEach((slot, i) => {
    if (includeLocked || !slot.locked) slot.song = null;
  });
  state.services[svcId].slots.forEach((slot, i) => {
    if (!slot.song) slot.song = pick(slot.cat, usedKeys({ svc: svcId, i }));
  });
}

function freshState(sunday = upcomingSunday()) {
  state = { sunday, services: {} };
  for (const svc of SERVICES) {
    state.services[svc.id] = { include: true, slots: svc.steps.filter(s => s.song).map(s => ({ cat: s.song, song: null, locked: false })) };
  }
  for (const svc of SERVICES) rerollService(svc.id);
}

function normalizeState() {
  // Rebuild if the layout changed since the lineup was saved.
  if (!state || !state.services) return freshState();
  for (const svc of SERVICES) {
    const cats = svc.steps.filter(s => s.song).map(s => s.song);
    const st = state.services[svc.id];
    if (!st || st.slots.length !== cats.length) {
      state.services[svc.id] = { include: true, slots: cats.map(cat => ({ cat, song: null, locked: false })) };
      rerollService(svc.id);
    }
  }
  if (!state.sunday) state.sunday = upcomingSunday();
}

// ---------- email text ----------
function songLine(s) {
  let line = `  ${s.number ? s.number.padEnd(4) : '    '} ${s.title}`;
  if (s.verses) line += ` (Vss ${s.verses})`;
  if (s.chorus) line += ', CHORUS once at end only';
  return line;
}

function includedServices() {
  return SERVICES.filter(svc => state.services[svc.id].include);
}

function walk(svc, onEvent, onSong) {
  let n = 0;
  for (const step of svc.steps) {
    if (step.event) onEvent(step.event);
    else onSong(state.services[svc.id].slots[n], n++);
  }
}

const subject = () => `Songs--${longDate(state.sunday)}`;

function emailText() {
  return includedServices().map(svc => {
    const lines = [`${svc.name}:`];
    walk(svc, ev => lines.push(ev), slot => slot.song && lines.push(songLine(slot.song)));
    return lines.join('\n');
  }).join('\n\n__________________________________________\n\n');
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function emailHtml() {
  const blocks = includedServices().map(svc => {
    const rows = [];
    walk(svc,
      ev => rows.push(`<tr><td colspan="2" style="padding:10px 0 4px;font-size:11px;letter-spacing:.08em;color:#6b665d;font-weight:bold">${escapeHtml(ev)}</td></tr>`),
      slot => {
        const s = slot.song; if (!s) return;
        const extra = [s.verses && `Verses ${s.verses.split(' ').join(', ')}`, s.chorus && 'chorus once at end only'].filter(Boolean).join(' · ');
        rows.push(`<tr><td style="padding:3px 12px 3px 0;font-weight:bold;color:#2f5d50;vertical-align:top;width:40px">${escapeHtml(s.number)}</td><td style="padding:3px 0">${escapeHtml(s.title)}${extra ? `<div style="font-size:12px;color:#6b665d">${escapeHtml(extra)}</div>` : ''}</td></tr>`);
      });
    return `<h2 style="font-size:17px;margin:18px 0 4px;color:#1f1d1a">${escapeHtml(svc.name)}</h2><table style="border-collapse:collapse;font-size:15px">${rows.join('')}</table>`;
  });
  return `<div style="font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1f1d1a">${blocks.join('<hr style="border:0;border-top:1px solid #e2ddd2;margin:18px 0">')}</div>`;
}

// ---------- rendering ----------
function duplicateKeys() {
  const counts = {};
  for (const svc of includedServices()) for (const slot of state.services[svc.id].slots) {
    if (slot.song) counts[keyOf(slot.song)] = (counts[keyOf(slot.song)] || 0) + 1;
  }
  return new Set(Object.keys(counts).filter(k => counts[k] > 1));
}

let dragFrom = null;

function render() {
  const dups = duplicateKeys();
  const root = $('#services');
  root.replaceChildren(...SERVICES.map(svc => renderService(svc, dups)));
  const warn = $('#warning');
  warn.hidden = dups.size === 0;
  warn.textContent = dups.size ? `Heads up: a song appears more than once this week (highlighted).` : '';
  $('#sunday').value = state.sunday;
  $('#subject').textContent = `Subject: ${subject()}`;
  $('#preview').textContent = emailText();
  renderChips();
  persist();
}

function renderService(svc, dups) {
  const st = state.services[svc.id];
  const include = el('input', { type: 'checkbox', checked: st.include, title: 'Include this service in the email' });
  include.addEventListener('change', () => { st.include = include.checked; render(); });

  const reroll = el('button', { className: 'btn small', textContent: '🎲', title: `New songs for ${svc.name} (keeps locked songs)` });
  reroll.addEventListener('click', () => { rerollService(svc.id); render(); });

  const list = el('ol', { className: 'steps' });
  walk(svc,
    ev => list.append(el('li', { className: 'event', textContent: ev })),
    (slot, i) => list.append(renderSong(svc, slot, i, dups)));

  return el('article', { className: `card${st.include ? '' : ' excluded'}` },
    el('div', { className: 'card-head' },
      el('h2', { textContent: svc.name }),
      el('div', { className: 'card-tools' }, el('label', { className: 'check muted' }, include, 'Include'), reroll)),
    list);
}

function renderSong(svc, slot, i, dups) {
  const s = slot.song || { title: '(no song)', number: '—', verses: '', chorus: false, note: '' };
  const slots = state.services[svc.id].slots;
  const li = el('li', { className: `song${slot.locked ? ' locked' : ''}${slot.song && dups.has(keyOf(slot.song)) ? ' dup' : ''}`, draggable: true });

  li.addEventListener('dragstart', e => { dragFrom = { svc: svc.id, i }; e.dataTransfer.effectAllowed = 'move'; });
  li.addEventListener('dragover', e => { if (dragFrom?.svc === svc.id) { e.preventDefault(); li.classList.add('drag-over'); } });
  li.addEventListener('dragleave', () => li.classList.remove('drag-over'));
  li.addEventListener('drop', e => {
    e.preventDefault();
    if (dragFrom?.svc === svc.id && dragFrom.i !== i) swap(slots, dragFrom.i, i);
    dragFrom = null; render();
  });

  const verses = el('button', { type: 'button', className: `pill${s.verses ? ' on' : ''}`, textContent: s.verses ? `Vss ${s.verses}` : 'All vss', title: 'Choose verses' });
  verses.addEventListener('click', () => {
    const input = el('input', { type: 'text', className: 'verses-input', value: s.verses, placeholder: '1 2 4' });
    let finished = false;
    const done = commit => {
      if (finished) return;
      finished = true;
      if (commit && slot.song) slot.song.verses = input.value.split(/[\s,]+/).filter(Boolean).join(' ');
      render();
    };
    input.addEventListener('keydown', e => { if (e.key === 'Enter') done(true); if (e.key === 'Escape') done(false); });
    input.addEventListener('blur', () => done(true));
    verses.replaceWith(input); input.focus(); input.select();
  });

  const chorus = el('button', { type: 'button', className: `pill${s.chorus ? ' on' : ''}`, textContent: 'Chorus at end', title: 'Toggle chorus once at end only' });
  chorus.addEventListener('click', () => { if (slot.song) { slot.song.chorus = !slot.song.chorus; render(); } });

  const btn = (icon, title, fn, disabled = false) => {
    const b = el('button', { type: 'button', className: 'btn small', textContent: icon, title, disabled });
    b.setAttribute('aria-label', title);
    b.addEventListener('click', fn);
    return b;
  };

  li.append(
    el('span', { className: 'num', textContent: s.number || '—', title: 'Drag to reorder' }),
    el('div', {},
      el('div', { className: 'title' }, s.title),
      el('div', { className: 'meta' },
        el('span', { className: 'cat', textContent: CATEGORY_LABELS[slot.cat] || slot.cat }),
        verses, chorus,
        s.note ? el('span', { className: 'pill note', textContent: s.note }) : null)),
    el('div', { className: 'actions' },
      btn('🎲', 'Random new song', () => { rerollSlot(svc.id, i); render(); }, slot.locked),
      btn('🔍', 'Search or enter a song', () => openPicker(svc, i)),
      btn(slot.locked ? '🔒' : '🔓', slot.locked ? 'Unlock (allow new lineup to replace)' : 'Lock (keep on new lineup)', () => { slot.locked = !slot.locked; render(); }),
      btn('↑', 'Move up', () => { swap(slots, i, i - 1); render(); }, i === 0),
      btn('↓', 'Move down', () => { swap(slots, i, i + 1); render(); }, i === slots.length - 1)));
  return li;
}

function swap(slots, a, b) {
  [slots[a].song, slots[b].song] = [slots[b].song, slots[a].song];
  [slots[a].locked, slots[b].locked] = [slots[b].locked, slots[a].locked];
}

// ---------- picker ----------
let pickerTarget = null;
let pickerSel = 0;

function openPicker(svc, i) {
  pickerTarget = { svc: svc.id, i };
  const slot = state.services[svc.id].slots[i];
  $('#picker-title').textContent = `Song ${i + 1} · ${svc.name} (${CATEGORY_LABELS[slot.cat] || slot.cat})`;
  $('#picker-q').value = '';
  $('#picker-all').checked = false;
  $('#m-title').value = ''; $('#m-number').value = ''; $('#m-verses').value = ''; $('#m-chorus').checked = false;
  showTab('search');
  renderPicker();
  $('#picker').showModal();
  $('#picker-q').focus();
}

function pickerResults() {
  const slot = state.services[pickerTarget.svc].slots[pickerTarget.i];
  const q = $('#picker-q').value.trim().toLowerCase();
  const source = $('#picker-all').checked ? allSongs : [...(pools[slot.cat] || [])].sort((a, b) => a.title.localeCompare(b.title));
  if (!q) return source;
  if (/^\d+$/.test(q)) return source.filter(s => s.number.startsWith(q)).sort((a, b) => (a.number === q ? -1 : b.number === q ? 1 : 0));
  return source.filter(s => s.title.toLowerCase().includes(q));
}

function renderPicker() {
  const used = usedKeys(pickerTarget);
  const recent = recentKeys();
  const results = pickerResults();
  pickerSel = Math.min(pickerSel, Math.max(0, results.length - 1));
  const ul = $('#picker-list');
  if (!results.length) {
    ul.replaceChildren(el('li', { className: 'empty', textContent: 'No matches. Try “All categories” or enter it manually.' }));
    return;
  }
  ul.replaceChildren(...results.slice(0, 400).map((s, idx) => {
    const tag = used.has(keyOf(s)) ? 'in use this week' : recent.has(keyOf(s)) ? 'sung recently' : ($('#picker-all').checked ? (CATEGORY_LABELS[s.cat] || s.cat) : '');
    const li = el('li', { className: `${idx === pickerSel ? 'sel' : ''}${used.has(keyOf(s)) ? ' used' : ''}`, role: 'option' },
      el('span', { className: 'n', textContent: s.number }), el('span', { textContent: s.title }), tag ? el('span', { className: 'tag', textContent: tag }) : null);
    li.addEventListener('click', () => choose(s));
    return li;
  }));
  ul.children[pickerSel]?.scrollIntoView({ block: 'nearest' });
}

function choose(song) {
  state.services[pickerTarget.svc].slots[pickerTarget.i].song = copySong(song);
  $('#picker').close();
  render();
}

function showTab(name) {
  document.querySelectorAll('#picker .tab').forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  document.querySelectorAll('#picker .tab-panel').forEach(p => (p.hidden = p.dataset.panel !== name));
}

// ---------- recipients ----------
const validEmail = s => /^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+$/.test(s);

function renderChips() {
  $('#chips').replaceChildren(...recipients.map(addr => {
    const x = el('button', { type: 'button', textContent: '×', title: `Remove ${addr}` });
    x.setAttribute('aria-label', `Remove ${addr}`);
    x.addEventListener('click', () => { recipients = recipients.filter(r => r !== addr); save(STORE.recipients, recipients); renderChips(); });
    return el('span', { className: 'chip' }, addr, x);
  }));
}

function addRecipients(text) {
  const bad = [];
  for (const raw of text.split(/[,;\s]+/).map(s => s.trim()).filter(Boolean)) {
    if (!validEmail(raw)) bad.push(raw);
    else if (!recipients.includes(raw.toLowerCase())) recipients.push(raw.toLowerCase());
  }
  save(STORE.recipients, recipients);
  renderChips();
  return bad;
}

// ---------- shared history ----------
const historyUrl = () => (prefs.historyUrl || CONFIG.historyUrl || '').trim();

async function loadSharedHistory() {
  const url = historyUrl();
  if (!url) { shared = { status: 'off', history: {} }; return; }
  try {
    const res = await fetch(`${url}${url.includes('?') ? '&' : '?'}weeks=26`);
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || 'bad response');
    const out = {};
    for (const [day, songs] of Object.entries(data.history || {})) out[day] = songs.map(keyOf);
    shared = { status: 'ok', history: out };
  } catch (err) {
    console.warn('Shared history unavailable:', err);
    shared = { status: 'error', history: {} };
  }
}

async function saveSharedHistory() {
  const url = historyUrl();
  if (!url) return true;
  const payload = {
    sunday: state.sunday,
    recipients,
    services: includedServices().map(svc => ({
      name: svc.name,
      songs: state.services[svc.id].slots.filter(sl => sl.song).map(sl => sl.song),
    })),
  };
  try {
    // text/plain keeps this a "simple" request, which Apps Script accepts without a CORS preflight.
    const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) });
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || 'bad response');
    shared.history[state.sunday] = [...usedKeys()];
    return true;
  } catch (err) {
    console.warn('Could not save shared history:', err);
    return false;
  }
}

// ---------- sending ----------
function emailjsSettings() {
  const base = CONFIG.emailjs || {};
  const o = prefs.emailjs || {};
  return { serviceId: o.serviceId || base.serviceId, templateId: o.templateId || base.templateId, publicKey: o.publicKey || base.publicKey };
}

function setStatus(text, kind = '') {
  const s = $('#send-status');
  s.textContent = text; s.className = `status ${kind}`;
}

async function send() {
  const pending = $('#recipient-input').value.trim();
  if (pending) {
    const bad = addRecipients(pending);
    $('#recipient-input').value = bad.join(', ');
    if (bad.length) return setStatus(`Not a valid address: ${bad.join(', ')}`, 'err');
  }
  if (!recipients.length) return setStatus('Add at least one recipient first.', 'err');
  if (!includedServices().length) return setStatus('Include at least one service.', 'err');
  const ej = emailjsSettings();
  if (!ej.serviceId || !ej.templateId || !ej.publicKey) return setStatus('Email isn’t set up yet. Add the EmailJS keys in Settings (⚙️).', 'err');
  if (!confirm(`Send “${subject()}” to ${recipients.join(', ')}?`)) return;

  const button = $('#send');
  button.disabled = true; setStatus('Sending…');
  try {
    const res = await fetch(EMAILJS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        service_id: ej.serviceId,
        template_id: ej.templateId,
        user_id: ej.publicKey,
        template_params: {
          to_email: recipients.join(', '),
          subject: subject(),
          message: emailText(),
          message_html: emailHtml(),
          reply_to: CONFIG.replyTo || '',
          sunday: longDate(state.sunday),
        },
      }),
    });
    const body = await res.text();
    if (!res.ok) throw new Error(body || `HTTP ${res.status}`);
    history[state.sunday] = [...usedKeys()];
    save(STORE.history, history);
    const logged = await saveSharedHistory();
    const sent = `Sent to ${recipients.length} recipient${recipients.length > 1 ? 's' : ''} ✓`;
    setStatus(logged ? sent : `${sent} (but the shared song history couldn’t be updated)`, logged ? 'ok' : 'err');
    toast('Email sent');
  } catch (err) {
    setStatus(`Send failed: ${err.message}`, 'err');
  } finally {
    button.disabled = false;
  }
}

// ---------- misc ----------
let toastTimer;
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 2200);
}

function openSettings() {
  $('#avoid-weeks').value = prefs.avoidWeeks;
  const ej = prefs.emailjs || {};
  $('#ej-service').value = ej.serviceId || '';
  $('#ej-template').value = ej.templateId || '';
  $('#ej-key').value = ej.publicKey || '';
  const base = CONFIG.emailjs || {};
  $('#ej-state').textContent = base.serviceId && base.templateId && base.publicKey
    ? 'Deployed keys are present. Leave these blank to use them.'
    : 'No deployed keys found. Add the GitHub secrets, or enter keys here.';
  $('#history-url').value = prefs.historyUrl || '';
  const weeks = [...new Set([...Object.keys(history), ...Object.keys(shared.history)])].sort().reverse();
  const source = { ok: 'Shared history is connected, so sends from every device count.', error: 'Shared history couldn’t be reached; using this device’s history only.', off: 'Shared history isn’t set up, so only sends from this device count.' }[shared.status];
  $('#history-summary').textContent = `${source} ${weeks.length ? `${weeks.length} sent week${weeks.length > 1 ? 's' : ''} on record, latest ${longDate(weeks[0])}.` : 'No song history yet.'}`;
  $('#settings').showModal();
}

function wire() {
  $('#church').textContent = CHURCH;
  $('#sunday').addEventListener('change', e => { if (e.target.value) { state.sunday = e.target.value; render(); } });
  $('#reroll-all').addEventListener('click', () => {
    for (const svc of SERVICES) state.services[svc.id].slots.forEach(s => { if (!s.locked) s.song = null; });
    for (const svc of SERVICES) rerollService(svc.id);
    render(); toast('New lineup');
  });
  $('#open-settings').addEventListener('click', openSettings);

  $('#recipient-form').addEventListener('submit', e => {
    e.preventDefault();
    const bad = addRecipients($('#recipient-input').value);
    $('#recipient-input').value = bad.join(', ');
    if (bad.length) setStatus(`Not a valid address: ${bad.join(', ')}`, 'err'); else setStatus('');
  });

  $('#copy').addEventListener('click', async () => {
    const text = `${subject()}\n\n${emailText()}`;
    try { await navigator.clipboard.writeText(text); toast('Copied to clipboard'); }
    catch { toast('Copy failed. Select the preview text instead.'); }
  });
  $('#print').addEventListener('click', () => window.print());
  $('#send').addEventListener('click', send);

  // picker
  document.querySelectorAll('#picker .tab').forEach(t => t.addEventListener('click', () => showTab(t.dataset.tab)));
  $('#picker-q').addEventListener('input', () => { pickerSel = 0; renderPicker(); });
  $('#picker-all').addEventListener('change', () => { pickerSel = 0; renderPicker(); });
  $('#picker-q').addEventListener('keydown', e => {
    const results = pickerResults();
    if (e.key === 'ArrowDown') { e.preventDefault(); pickerSel = Math.min(pickerSel + 1, results.length - 1); renderPicker(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); pickerSel = Math.max(pickerSel - 1, 0); renderPicker(); }
    if (e.key === 'Enter') { e.preventDefault(); if (results[pickerSel]) choose(results[pickerSel]); }
  });
  $('#m-save').addEventListener('click', () => {
    const title = $('#m-title').value.trim();
    if (!title) { $('#m-title').focus(); return; }
    choose({ title: titleCase(title), number: $('#m-number').value.trim(), verses: $('#m-verses').value.split(/[\s,]+/).filter(Boolean).join(' '), chorus: $('#m-chorus').checked, note: '' });
  });

  // settings
  $('#save-settings').addEventListener('click', () => {
    prefs.avoidWeeks = Math.max(0, Math.min(26, Number($('#avoid-weeks').value) || 0));
    const oldUrl = historyUrl();
    prefs.historyUrl = $('#history-url').value.trim();
    if (historyUrl() !== oldUrl) loadSharedHistory();
    prefs.emailjs = { serviceId: $('#ej-service').value.trim(), templateId: $('#ej-template').value.trim(), publicKey: $('#ej-key').value.trim() };
    save(STORE.prefs, prefs);
    toast('Settings saved');
  });
  $('#clear-history').addEventListener('click', () => {
    if (!confirm('Forget which songs were sent from this device? (The shared Google Sheet is not changed.)')) return;
    history = {}; save(STORE.history, history); openSettings();
  });
  $('#start-over').addEventListener('click', () => {
    if (!confirm('Throw away this lineup and start fresh?')) return;
    freshState(state.sunday); $('#settings').close(); render();
  });
}

async function main() {
  wire();
  await Promise.all([loadSongs(), loadSharedHistory()]);
  normalizeState();
  render();
}

main();

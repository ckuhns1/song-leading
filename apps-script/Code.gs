// Shared song history for the Melody web app.
// Paste this into Extensions → Apps Script of a Google Sheet, then
// Deploy → New deployment → Web app (Execute as: Me, Who has access: Anyone).
// The web app URL goes in the repository secret HISTORY_URL.

const SHEET_NAME = 'History';
const HEADERS = ['Sent at', 'Sunday', 'Service', 'Position', 'Number', 'Title', 'Verses', 'Chorus at end', 'Recipients'];

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    sh.getRange('B:B').setNumberFormat('@');  // keep Sunday as plain YYYY-MM-DD text
  }
  return sh;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// GET ?weeks=26 → { ok, history: { 'YYYY-MM-DD': [{ number, title }] } }
function doGet(e) {
  const weeks = Math.min(Number(e.parameter.weeks) || 26, 104);
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - (weeks + 1) * 7);
  const cutoffIso = Utilities.formatDate(cutoff, 'UTC', 'yyyy-MM-dd');

  const history = {};
  const rows = sheet_().getDataRange().getDisplayValues().slice(1);
  for (const r of rows) {
    const sunday = r[1];
    if (!/^\d{4}-\d{2}-\d{2}$/.test(sunday) || sunday < cutoffIso) continue;
    (history[sunday] = history[sunday] || []).push({ number: r[4], title: r[5] });
  }
  return json_({ ok: true, history });
}

// POST (text/plain body) { sunday, recipients: [], services: [{ name, songs: [{ number, title, verses, chorus }] }] }
// Replaces any rows already logged for that Sunday, so a re-send keeps the final list.
function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const data = JSON.parse(e.postData.contents);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(data.sunday || '')) return json_({ ok: false, error: 'bad sunday' });

    const sh = sheet_();
    const values = sh.getDataRange().getDisplayValues();
    for (let i = values.length - 1; i >= 1; i--) {
      if (values[i][1] === data.sunday) sh.deleteRow(i + 1);
    }

    const now = new Date();
    const recipients = (data.recipients || []).join(', ');
    const rows = [];
    for (const svc of data.services || []) {
      (svc.songs || []).forEach((s, i) => {
        rows.push([now, data.sunday, String(svc.name || ''), i + 1, String(s.number || ''), String(s.title || ''), String(s.verses || ''), s.chorus ? 'yes' : '', recipients]);
      });
    }
    if (rows.length) sh.getRange(sh.getLastRow() + 1, 1, rows.length, HEADERS.length).setValues(rows);
    return json_({ ok: true, saved: rows.length });
  } finally {
    lock.releaseLock();
  }
}

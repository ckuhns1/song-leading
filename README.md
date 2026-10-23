# Worship Assembly Song Selector

This application automates the creation and curation of song lists for the assembly of the church. It generates randomized lineups from Praise for the Lord (c) customized to their congregation's order of worship, reviews and revises song selections interactively, and exports the finalized order via email.

## 📦 Features

- Draws from a repository of categorized songs
- Automatically select songs for each part of the service
- Interactive revisions:
  - Randomly replace a song
  - Search and manually choose a replacement
  - Manually specify custom song info
- Email service orders in a formatted layout

---

## 🛠️ Project Structure

```
project/
│
├── domain/
│   └── assembly.py        # Song and Service class definitions
│
├── customize/
│   └── service_layouts.py  # Service design (AM/PM song and event mappings)
│   └── connection.py      # Email info for sending songs
│
├── service/
│   ├── email.py          # Email handling and preview
│   └── repository.py     # Song pool for different song groups
│
├── master.py             # Main script to run app and email results
├── README.md             # You're here!
```

---

## 🌐 Web App (GitHub Pages)

The `web/` folder is a static web app ("Melody") that does everything the terminal app does, in the browser:

- Random lineup for Sunday AM, Sunday PM and Wednesday, with no song repeated across the week
- Per-song reroll, search by title or number, manual entry, verses, chorus-at-end, reorder (drag or arrows), and lock
- Avoids songs sent in the last few weeks (history kept in the browser)
- Recipients remembered on the device; preview, copy, print, and one-click send through [EmailJS](https://www.emailjs.com)

The songs come straight from `songs_app/infra/*.csv`, and the order of worship lives in `web/layouts.js`.
Every push to `main` that touches `web/` or the CSVs deploys the site with `.github/workflows/pages.yml`.

### One-time setup

1. **Turn on Pages:** repo Settings → Pages → Source: **GitHub Actions**. (Pages on a private repo needs a paid GitHub plan; otherwise make the repo public.)
2. **EmailJS:** create a free account at emailjs.com, then
   - Email Services → Add Service → Gmail, and sign in as the sending account. Note the **Service ID**.
   - Email Templates → Create Template. Set **To Email** to `{{to_email}}`, **Subject** to `{{subject}}`, **Reply To** to `{{reply_to}}`, and the body (in the code editor) to `{{{message_html}}}`. Note the **Template ID**.
   - Account → General: copy the **Public Key**. Under Account → Security, add your Pages address (e.g. `https://ckuhns1.github.io`) to the allowed domains so nobody else can use your quota.
3. **Secrets:** repo Settings → Secrets and variables → Actions → New repository secret: `EMAILJS_SERVICE_ID`, `EMAILJS_TEMPLATE_ID`, `EMAILJS_PUBLIC_KEY`. Then rerun the "Deploy web app to GitHub Pages" workflow (Actions tab → Run workflow).

4. **Shared song history (optional, recommended when several people send):**
   - Create a Google Sheet (e.g. "Melody song history"), then Extensions → Apps Script.
   - Replace the editor contents with `apps-script/Code.gs`, save, then Deploy → New deployment → type **Web app**, Execute as **Me**, Who has access **Anyone** → Deploy, and authorize.
   - Copy the web app URL (ends in `/exec`) into a repository secret `HISTORY_URL`, then rerun the deploy workflow.
   - Every send then logs its songs to the sheet's History tab, and every device avoids songs sent recently from any device.

The EmailJS public key is meant to be public (it ends up in the page), so the domain allowlist is what protects it. No Gmail app password is needed for the web app.

### Run locally

```
mkdir -p /tmp/site/songs && cp -r web/. /tmp/site/ && cp songs_app/infra/*.csv /tmp/site/songs/
python3 -m http.server -d /tmp/site 8000
```

Then open http://localhost:8000 and enter the EmailJS keys under ⚙️ Settings.

---

## 🖥️ Terminal App

## 🚀 Getting Started

### 1. Install Requirements
No external packages are required beyond Python 3.x.

### 2. Run the application driver script

```
python master.py
```

You will be prompted to:
- Review a proposed list of songs for the morning and evening services.
- Make changes using these commands:
  - `#` : Change that song to a random new one
  - `#*` : Search for a song containing a word and choose from matches
  - `#-` : Manually enter a song title, number, and verses
  - `y` : Accept the current list and move on

After all services (e.g., Sunday AM & PM) are confirmed, the program previews the full email body and sends it upon receiving user confirmation.

---

## ✍️ Customizing for Your Church

To adapt this app for your congregation:
1. Create a new class in `customize/service_layouts.py` following the `Hillview` example, or modify that example.
2. Define:
   - `am_songs`, `pm_songs`: Mapping of service parts to song types
   - `am_events`, `pm_events`: Ordered service events and how many songs occur before the next event
3. Add the new layout class to the main driver script (`master.py`).

---

## ✉️ Email Delivery

Email preview and sending are handled via the `Email` class in `service/email.py`. Configure the source & destination addresses in customize/connection.py. (A an app password (from gmail, other) is required to set up sending from an email account.)

---

## 🧩 Example Output

```
Sunday AM:
OPENING PRAYER
  345 Holy, Holy, Holy (Vss 1 2 4), CHORUS once at end only
COLLECTION
  123 Just As I Am
...
Sunday PM:
...
```

---

## 📬 Contact

Created by Chad Kuhns `chalkuhns@gmail.com' for use by the Hillview Terrace church of Christ. Adapt and use freely for your congregation.

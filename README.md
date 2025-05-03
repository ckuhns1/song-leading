# Worship Assembly Song Selector

This Python application helps automate the creation and curation of song lists for the assembly of the church. It allows a user to generate randomized lineups customized to their congregation's order of worship, review and revise song selections interactively, and export the finalized order via email.

## 📦 Features

- Load service templates for AM and PM services (e.g., Hillview layout--see design/service_layouts.py)
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
│   └── assembly.py       # Song and Service class definitions
│
├── design/
│   └── service_layouts.py  # Layouts like Hillview (AM/PM song and event mappings)
│
├── service/
│   ├── email.py          # Email handling and preview
│   └── repository.py     # Song pool for different song groups
│
├── master.py             # Main script to run app and email results
├── README.md             # You're here!
```

---

## 🚀 Getting Started

### 1. Install Requirements
No external packages are required beyond Python 3.x.

### 2. Run the Application

```bash
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

To adapt this app for another congregation:
1. Create a new class in `design/service_layouts.py` following the `Hillview` example.
2. Define:
   - `am_songs`, `pm_songs`: Mapping of service parts to song types
   - `am_events`, `pm_events`: Ordered service events and how many songs occur before each
3. Add the new layout to the main driver script (`driver.py`).

---

## ✉️ Email Delivery

Email preview and sending are handled via the `Email` class in `service/email.py`. You can configure the destination address there or in the driver script. (A an app password (from gmail, other) is required to set up sending from one's own address.)

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

Created by Chad Kuhns for use by the Hillview Terrace church of Christ. Adapt and reuse freely for other congregations!

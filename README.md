# ASTRAVITA: Astronaut Health Monitoring Platform

**Team:** ASTRAVITA SpaceLab | **Event:** NASA Space Apps Challenge 2026
**Stack:** Python, Streamlit, Pandas, Plotly

> ⚠️ **SIMULATED DATA.** Every number in this app is generated for demonstration only.
> No real medical data is used, and the alerts are statistical checks, not medical advice.

---

## 1. How to run (Windows)

You only need to do steps 1 to 3 once.

```bat
:: 1) Open "Command Prompt" (cmd, not PowerShell) inside the project folder
cd C:\path\to\astravita

:: 2) Create a virtual environment and turn it on
python -m venv venv
venv\Scripts\activate

:: 3) Install the libraries
pip install -r requirements.txt

:: 4) Run the app (do this every time)
streamlit run app.py
```

The app opens at **http://localhost:8501**. To stop it, press **Ctrl + C** in the terminal.

> Python files reload with **F5** in the browser.
> If you change `ui_theme.py` or `.streamlit/config.toml`, restart the app: press Ctrl + C, then run `streamlit run app.py` again.

---

## 2. Project files and owners

```
astravita/
├── app.py                 UI team: all pages and navigation (the main file)
├── ui_theme.py            UI team: colors, fonts, animated logo, responsive CSS
├── data.py                Data team: astronauts + health data   (temporary version)
├── health_analysis.py     Analysis team: baseline + alerts       (temporary version)
├── equipment_guide.py     Equipment team: medical equipment list (temporary version)
├── images/
│   ├── logo.png           full ASTRAVITA logo
│   ├── logo_mark.png      the "A" mark used in the top bar and browser tab
│   └── AST-01.jpg ...     (optional) astronaut photos; initials are shown if missing
├── .streamlit/config.toml dark theme settings
└── requirements.txt
```

The three team files contain **working temporary versions** so that the app runs today.
Each team can replace its file with the real one, **as long as it keeps the function names and data shapes in section 3**.

---

## 3. Data contract

These are the rules every team must follow. If you keep them, the UI keeps working with no changes.

### `data.py`

| Function | Returns |
|---|---|
| `get_astronauts()` | `list[dict]`, one dict per astronaut |
| `get_health_data(astronaut_id)` | `pandas.DataFrame`, one row per day, oldest day first |

**Keys of each astronaut dict:**

| Key | Type | Example |
|---|---|---|
| `id` | str | `"AST-02"` |
| `name` | str | `"Mohammed Baqir"` |
| `role` | str | `"Flight Engineer"` |
| `age` | int | `36` |
| `mission` | str | `"ASTRAVITA-1"` |
| `mission_day` | int | `30` |
| `photo` | str | `"images/AST-02.jpg"` (the file can be missing) |

**Columns of the health DataFrame:**

| Column | Unit | Type |
|---|---|---|
| `date` | day | datetime64 |
| `heart_rate` | bpm | float |
| `sleep_hours` | hours | float |
| `activity_minutes` | minutes | float |
| `spo2` | % | float |
| `body_temp` | °C | float |

### `health_analysis.py`

| Function | Returns |
|---|---|
| `calculate_baseline(df)` | `{metric: {"mean", "std", "low", "high"}}` for the 5 metrics above |
| `detect_alerts(df, baseline)` | `list[dict]`, sorted with **critical** alerts first; an empty list means no alerts |

**Keys of each alert dict:** `date`, `metric` (a column name), `value`, `severity` (`"critical"` or `"warning"`), `message` (short title), `explanation` (full sentence for the user), `baseline_mean`.

**Current rule (temporary):**
- The personal baseline is calculated from all days **before** the last 7 days.
- A **warning** is raised when a reading is 2 standard deviations or more from the baseline.
- A **critical** alert is raised at 3 standard deviations or more.

This is a statistical rule, **not** a medical criterion.

### `equipment_guide.py`

| Function | Returns |
|---|---|
| `get_equipment_list()` | `list[dict]` |

**Keys of each device dict:** `name`, `category`, `purpose`, `steps` (list of str), `safety_notes`, `metrics` (list of column names this device measures, e.g. `["spo2", "heart_rate"]`; it can be empty).

The `metrics` key is what lets the Equipment Guide page show
**"Suggested for a current alert"** on the right devices.

---

## 4. Pages

| Page | What it shows |
|---|---|
| **Dashboard** | Astronaut card, today's 5 vital signs compared with their own average, and 30-day trend charts |
| **Astronaut Profile** | Personal details and personal baseline (normal value and usual range) for each metric |
| **Health Alerts** | Alerts with a "Why this alert?" explanation and a chart that shows the usual range |
| **Equipment Guide** | Search and category filter, how-to-use steps, and safety notes |
| **Health Reports** | Report preview, a printable HTML report (Ctrl + P saves it as PDF) and a CSV of the data |

**Crew (5 astronauts, simulated health data):** Jafar Alrubaiy (Mission Commander), Mohammed Baqir (Flight Engineer), Ali Mohammed (Science Officer), Ali Hasan (Flight Surgeon) and Taha Qasim (Mission Specialist).

**Demo tip:** choose **Mohammed Baqir**. His simulated data has 2 **critical** alerts (high heart rate and low sleep). **Ali Hasan** has 1 **warning** (blood oxygen a little low). The other three are stable.

---

## 5. Optional: astronaut photos

1. Put `AST-01.jpg` to `AST-05.jpg` in the `images/` folder.
2. If a photo is missing, the app shows the astronaut's initials instead.

---

## 6. Test checklist (all passed ✅)

- [x] All 5 pages open with no errors, for all 5 astronauts
- [x] Mohammed Baqir shows 2 critical alerts, Ali Hasan shows 1 warning, and the other three show none
- [x] The report HTML and CSV download
- [x] The layout works on a large screen (1440 px), a laptop or projector (1024 px) and a phone (375 px)
- [x] The animated logo appears in the top bar and in the browser tab
- [x] "Simulated Data" labels are shown in the top bar, the footer and the report

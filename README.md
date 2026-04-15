# 🧠 Mental Health Crisis Early-Warning System
### State-Level Prevalence Analyzer

A lightweight command-line application that **visualizes, analyzes, and predicts** state-level mental health crisis risk across the United States, using publicly available SAMHSA survey data.

Built as part of the **MSIM Community Resilience Intelligence Platform** project, this tool supports the *Information Story* from G3: people in mental health crisis often cannot find care — not because it doesn't exist, but because no one is watching the signals early enough.

---

## 📊 Data Source

**SAMHSA NSDUH 2023–2024 State Prevalence Tables**
- **Full name**: National Survey on Drug Use and Health (NSDUH)
- **Publisher**: Substance Abuse and Mental Health Services Administration (SAMHSA)
- **URL**: https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/state-releases
- **Direct download**: *2023–2024 State Prevalence Tables: CSV (ZIP)*
- **Format**: CSV — one row per U.S. state, 38 mental health and substance use measures
- **Coverage**: All 50 states + DC, civilian non-institutionalized population aged 12+
- **Update frequency**: Annual

### Information Structure

Each state record in the CSV contains:

| Field | Description |
|-------|-------------|
| `State` | Full state name |
| `State_Abbr` | Two-letter abbreviation |
| `Any_Mental_Illness_Pct` | % of population with any mental illness |
| `Serious_Mental_Illness_Pct` | % with serious mental illness |
| `Major_Depressive_Episode_Pct` | % with major depressive episode in past year |
| `Mental_Health_Treatment_Rate_Pct` | % receiving mental health treatment |

### Derived Fields (computed by the app)

| Field | Formula |
|-------|---------|
| `care_gap` | `any_mi_pct − (any_mi_pct × tx_rate / 100)` — % with MI who are NOT in treatment |
| `risk_score` | Weighted composite: 40% MI prevalence + 35% SMI prevalence + 25% care gap |
| `risk_tier` | 🔴 HIGH (≥65) / 🟡 MODERATE (48–64) / 🟢 LOW (<48) |

---

## 💡 What the App Does

The app answers three questions from our Information Story:

1. **Where is mental illness most prevalent?** → Full ranked table of all 50 states
2. **Where are people going untreated?** → Care Gap chart (unmet need by state)
3. **Where is a crisis surge most likely?** → Surge predictor flags states where `care_gap > 15%` AND `SMI > 9%`

---

## 🛠 Requirements

- Python 3.8 or higher
- No external libraries required — uses only Python standard library (`csv`, `statistics`, `argparse`)

---

## 📥 Installation & Setup

### 1. Clone or download the repository

```bash
git clone https://github.com/your-username/mental-health-early-warning.git
cd mental-health-early-warning
```

### 2. Get the data

**Option A — Use the included sample data (recommended for quick start)**

The file `nsduh_state_mental_health_2023.csv` is already included in the repository. It contains representative values matching the structure of the real NSDUH dataset.

**Option B — Download real SAMHSA data**

1. Go to: https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/state-releases
2. Under *2023–2024*, click **State Prevalence Tables: CSV (ZIP)**
3. Unzip and place the CSV file in the project folder
4. Update the column names in `app.py` to match SAMHSA's actual headers (see codebook PDF)

**Option C — Regenerate sample data**

```bash
python generate_sample_data.py
```

---

## ▶️ How to Run

### Full dashboard (all 50 states, care gap chart, surge prediction)
```bash
python app.py
```

### Single state report
```bash
python app.py --state WA
python app.py --state TX
python app.py --state NY
```

### High-risk states only + surge prediction
```bash
python app.py --risk
```

---

## 📋 Sample Output

```
════════════════════════════════════════════════════════════════════════
  🧠  MENTAL HEALTH CRISIS EARLY-WARNING SYSTEM
       State-Level Prevalence Analyzer | SAMHSA NSDUH 2023–2024
════════════════════════════════════════════════════════════════════════

  NATIONAL SUMMARY
  ────────────────────────────────────────────────────────────────────
  States analyzed          : 50
  Avg Any Mental Illness   : 20.5%
  Avg Serious MI           : 8.6%
  Avg Care Gap             : 9.2%
  High-risk states         : 12

  STATE REPORT: Washington (WA)
  ────────────────────────────────────────────────────────────────────
  Any Mental Illness          : 22.3%  ██████████████████████░░░░░░░░
  Serious Mental Illness      : 10.0%  ████████████████████░░░░░░░░░░
  Care Gap (untreated)        :  8.5%  ███████████░░░░░░░░░░░░░░░░░░░

  ► Risk Score : 107.6
  ► Risk Tier  : 🔴 HIGH

  ⚠  RECOMMENDATION: Pre-position mobile crisis teams.
```

---

## 📁 File Structure

```
mental-health-early-warning/
│
├── app.py                              # Main application
├── generate_sample_data.py             # Generates sample CSV data
├── nsduh_state_mental_health_2023.csv  # Data file (NSDUH structure)
└── README.md                           # This file
```

---

## 🔗 Connection to Project Theme

This app is the first layer of the **Mental Health Crisis Early-Warning System** described in our G3 Information Story. It operationalizes the *state-level prevalence signal* — the baseline layer that tells crisis coordinators which states are under the most structural pressure before individual surge events occur.

The care gap metric directly quantifies the gap between need and care that drives the story of callers placed on hold, mobile teams not pre-positioned, and communities left without resources.

**Next steps** for a more complete system would add:
- ZIP-code-level 211 call volume data (SAMHSA crisis line logs)
- Real-time social media distress signal feeds (Twitter/X NLP)
- Time-series forecasting for 2–4 week surge prediction

---

## 📚 Citation

> Substance Abuse and Mental Health Services Administration. (2024). *2023–2024 National Survey on Drug Use and Health (NSDUH): State Prevalence Tables*. Center for Behavioral Health Statistics and Quality. https://www.samhsa.gov/data

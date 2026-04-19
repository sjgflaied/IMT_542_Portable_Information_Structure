# Mental Health Crisis Early-Warning System

A command-line tool that analyzes state-level mental health prevalence data to identify where crisis risk is highest and where people are going untreated.

Built for the MSIM Community Resilience Intelligence Platform project.

---

## Data Source

SAMHSA NSDUH 2023-2024 State Prevalence Tables
https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/state-releases

The CSV file contains state-level estimates for mental illness prevalence, serious mental illness, major depressive episodes, and mental health treatment rates across all 50 states.

The app adds two derived fields:
- `care_gap`: percentage of people with mental illness who are not receiving treatment
- `risk_score`: weighted composite of prevalence and care gap used to rank states

---

## Requirements

Python 3.8 or higher. No external libraries needed.

---

## Setup

Clone the repository and enter the folder:

```bash
git clone https://github.com/your-username/mental-health-early-warning.git
cd mental-health-early-warning
```

The data file `nsduh_state_mental_health_2023.csv` is included. If you want to regenerate it:

```bash
python generate_sample_data.py
```

---

## How to Run

Full dashboard (all 50 states, care gap chart, surge prediction):
```bash
python app.py
```

Single state report:
```bash
python app.py --state WA
```

High-risk states and surge prediction only:
```bash
python app.py --risk
```

---

## Files

```
app.py                             # Main application
generate_sample_data.py            # Generates the sample CSV
nsduh_state_mental_health_2023.csv # Data file
README.md                          # This file
```

---

## Citation

Substance Abuse and Mental Health Services Administration. (2024). 2023-2024 National Survey on Drug Use and Health (NSDUH): State Prevalence Tables. https://www.samhsa.gov/data

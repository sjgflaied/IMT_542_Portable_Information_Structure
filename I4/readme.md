# Data Access Demo

Three information structures accessed via three different technologies — all runnable with a single command, no API keys, no manual file downloads.

| # | Structure | Access Technology | Source |
|---|-----------|------------------|--------|
| 1 | **JSON** | REST API over HTTP | Open-Meteo weather API |
| 2 | **HTML** | HTTP scraping (BeautifulSoup) | Wikipedia table |
| 3 | **CSV** | Direct URL download (streamed) | NYC Open Data 311 requests |

## Quick Start

```bash
# 1. Install dependencies (one-time)
pip install requests beautifulsoup4

# 2. Run
python fetch_data.py
```

That's it — no accounts, no API keys, no file downloads needed.

## What you'll see

```
DATA ACCESS DEMO — 3 structures × 3 technologies

============================================================
1. JSON via REST API — Open-Meteo current weather
============================================================
Location     : Seattle, WA  (47.6062°N, -122.3321°W)
Temperature  : 54.3 °F
...

============================================================
2. HTML via HTTP scraping — Wikipedia countries by area
============================================================
Rank   Country/Territory                   Total km²          Land km²
...

============================================================
3. CSV via URL download — NYC 311 Service Requests
============================================================
CREATED_DATE          COMPLAINT_TYPE               ...
...
```

## Pros & Cons (summary)

Detailed pros/cons are in comments inside `fetch_data.py`. Quick summary:

**JSON/REST API** — clean and structured, but fragile to API changes and subject to rate limits.

**HTML scraping** — works on any public page, but brittle to layout changes and disallowed on some sites.

**CSV download** — universally readable, but no enforced schema and potentially large files.

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`


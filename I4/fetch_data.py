"""
data_access_demo/fetch_data.py
==============================
Demonstrates three different information structures accessed via three
different technologies, all with zero API keys or manual downloads.

Requirements (install once):
    pip install requests beautifulsoup4

Run:
    python fetch_data.py
"""

import requests
import csv
import io
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# 1. JSON via REST API  —  Open-Meteo weather (no API key required)
# ---------------------------------------------------------------------------
#
# PROS:
#   + Structured, machine-readable data arrives ready to use (no parsing step).
#   + REST APIs are stateless and easy to call from any language or tool.
#   + Open-Meteo is free, requires no authentication, and is highly reliable.
#   + Query parameters let you request exactly the fields you need.
#
# CONS:
#   - Dependent on network availability and third-party uptime.
#   - Rate limits / quotas can throttle heavy usage.
#   - API schema can change without notice, breaking your code.
#   - Nested JSON structures can require careful traversal logic.
#
def fetch_weather_json():
    """
    Calls the Open-Meteo API for Seattle's current weather (JSON).
    Docs: https://open-meteo.com/en/docs
    """
    print("=" * 60)
    print("1. JSON via REST API — Open-Meteo current weather")
    print("=" * 60)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 47.6062,
        "longitude": -122.3321,
        "current": "temperature_2m,wind_speed_10m,precipitation,weather_code",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "America/Los_Angeles",
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    current = data["current"]
    units = data["current_units"]

    print(f"Location     : Seattle, WA  ({data['latitude']}°N, {data['longitude']}°W)")
    print(f"Timezone     : {data['timezone']}")
    print(f"Observed at  : {current['time']}")
    print(f"Temperature  : {current['temperature_2m']} {units['temperature_2m']}")
    print(f"Wind speed   : {current['wind_speed_10m']} {units['wind_speed_10m']}")
    print(f"Precipitation: {current['precipitation']} {units['precipitation']}")
    print(f"Weather code : {current['weather_code']}  (WMO code — 0=clear, 61=rain, 71=snow …)")
    print()


# ---------------------------------------------------------------------------
# 2. HTML via HTTP scraping  —  Wikipedia "List of countries by population"
# ---------------------------------------------------------------------------
#
# PROS:
#   + Works for any public web page — no API or account needed.
#   + BeautifulSoup makes navigating the DOM straightforward.
#   + Extremely flexible: you can pull text, tables, links, images, etc.
#
# CONS:
#   - Fragile — HTML structure can change at any time without warning.
#   - Legally/ethically grey for some sites (check robots.txt / ToS).
#   - No schema guarantee; you must inspect the page to find the right
#     selectors, which is tedious and brittle.
#   - Dynamic (JavaScript-rendered) pages require heavier tools like
#     Playwright or Selenium; BeautifulSoup alone won't work there.
#
def fetch_wikipedia_html():
    """
    Scrapes the Wikipedia 'List of countries by area' page (HTML).
    Extracts the first 10 rows of the main sortable table.
    """
    print("=" * 60)
    print("2. HTML via HTTP scraping — Wikipedia countries by area")
    print("=" * 60)

    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
    headers = {"User-Agent": "data-access-demo/1.0 (educational project)"}

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # The first wikitable on the page is the countries-by-area table
    table = soup.find("table", class_="wikitable")
    rows = table.find_all("tr")

    # Print header
    header_cells = rows[0].find_all(["th", "td"])
    headers_text = [c.get_text(strip=True) for c in header_cells]
    # Keep only the first 4 columns for readability
    print(f"{'Rank':<6} {'Country/Territory':<35} {'Total km²':<18} {'Land km²'}")
    print("-" * 75)

    for row in rows[1:11]:          # first 10 data rows
        cells = row.find_all(["th", "td"])
        if len(cells) < 4:
            continue
        cols = [c.get_text(strip=True) for c in cells]
        rank    = cols[0]
        country = cols[1][:34]      # trim long names
        total   = cols[2]
        land    = cols[3]
        print(f"{rank:<6} {country:<35} {total:<18} {land}")

    print()


# ---------------------------------------------------------------------------
# 3. CSV via direct URL download  —  NYC 311 Service Requests (Open Data)
# ---------------------------------------------------------------------------
#
# PROS:
#   + CSV is universally supported — open in Excel, pandas, R, or plain Python.
#   + NYC Open Data publishes stable, well-documented export URLs.
#   + Streaming with iter_lines() means you never load the full (huge) file
#     into memory; you can stop after N rows.
#   + No authentication required for public datasets.
#
# CONS:
#   - CSV has no enforced schema — column types are all strings by default.
#   - Large files are slow to download; streaming helps but adds complexity.
#   - The dataset can be updated or restructured by the publisher.
#   - Filtering happens client-side (or via Socrata SODA query params), unlike
#     SQL where filtering is pushed to the server.
#
def fetch_nyc_csv():
    """
    Streams a CSV of recent NYC 311 complaints directly from NYC Open Data.
    Prints a sample of the first 10 rows without downloading the whole file.
    Dataset: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
    We use the Socrata SODA API endpoint with a row limit for speed.
    """
    print("=" * 60)
    print("3. CSV via URL download — NYC 311 Service Requests")
    print("=" * 60)

    # $limit=15 keeps the download tiny; remove or increase for real work
    url = (
        "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
        "?$limit=15&$order=created_date%20DESC"
    )
    headers = {"Accept": "text/csv"}

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    reader = csv.DictReader(io.StringIO(resp.text))
    rows = list(reader)

    # Show a few meaningful columns
    cols = ["created_date", "complaint_type", "descriptor", "borough", "status"]
    col_widths = [20, 28, 28, 13, 10]

    header_line = "  ".join(c.upper().ljust(w) for c, w in zip(cols, col_widths))
    print(header_line)
    print("-" * sum(col_widths + [2 * (len(cols) - 1)]))

    for row in rows[:10]:
        line = "  ".join(
            str(row.get(c, "N/A"))[:w].ljust(w) for c, w in zip(cols, col_widths)
        )
        print(line)

    print(f"\n(Showing 10 of {len(rows)} rows fetched; full dataset has millions of records)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n🔍  DATA ACCESS DEMO — 3 structures × 3 technologies\n")
    fetch_weather_json()
    fetch_wikipedia_html()
    fetch_nyc_csv()
    print("✅  Done.")

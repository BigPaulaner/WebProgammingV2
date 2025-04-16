"""
World Bank Indicator Explorer

This script retrieves all available indicators from the World Bank API via RapidAPI
and then fetches historical data for a specified country.

API used:
- World Bank Development Indicators via RapidAPI
"""

import requests
import time

headers = {
    "x-rapidapi-key": "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061",
    "x-rapidapi-host": "word-bank-world-development-indicators.p.rapidapi.com"
}

# Step 1: Fetch all indicators via pagination
all_indicators = []
page = 1

while True:
    indicators_url = f"https://word-bank-world-development-indicators.p.rapidapi.com/indicators?page={page}&pageSize=100"
    response = requests.get(indicators_url, headers=headers, verify=False)

    if response.status_code != 200:
        print(f"❌ Error loading page {page}: {response.status_code}")
        break

    data = response.json()
    indicators = data.get("indicators", [])
    if not indicators:
        break

    all_indicators.extend(indicators)
    print(f"📄 Page {page}: {len(indicators)} indicators loaded.")
    page += 1
    time.sleep(0.5)

print(f"\n➡️ Total indicators found: {len(all_indicators)}\n")

# Step 2: Retrieve data per indicator for a specific country
country_code = "DE"  # Example: Germany

for idx, indicator in enumerate(all_indicators, start=1):
    indicator_code = indicator.get("id")
    indicator_name = indicator.get("indicator")

    if not indicator_code:
        continue

    url = f"https://word-bank-world-development-indicators.p.rapidapi.com/country/{country_code}/indicator/{indicator_code}"
    resp = requests.get(url, headers=headers, verify=False)

    if resp.status_code == 200:
        country_data = resp.json()
        print(f"📊 {idx}/{len(all_indicators)} - {indicator_name} ({indicator_code})")
        for entry in country_data.get("indicators", []):
            print(f"{entry.get('date')}: {entry.get('value')}")
        print("-" * 40)
    else:
        print(f"⚠️ Error retrieving {indicator_code}: {resp.status_code}")

    time.sleep(0.5)  # Delay to avoid rate limiting
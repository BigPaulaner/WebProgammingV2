"""
Cost of Living Module

Retrieves and processes cost of living data for a given city and country using the
"Cost of Living and Prices" API on RapidAPI.

API used:
- https://rapidapi.com/karnadi/api/cost-of-living-and-prices/
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061"

# Mapping of product categories to API good IDs
CATEGORIES = {
    "Real Estate (€/m²)": [1, 2],
    "Clothing": [5, 6, 7, 64],
    "Groceries": [9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27],
    "Rent": [28, 29, 30, 31],
    "Restaurants": [36, 37, 38],
    "Gasoline": [45],
    "Public Transport Pass": [46],
    "Utilities": [54],
    "Internet (60 Mbps)": [55]
}

# Value normalization ranges for scoring
NORMALIZATION_RANGES = {
    "Real Estate (€/m²)": (1000, 10000),
    "Clothing": (20, 150),
    "Groceries": (1, 10),
    "Rent": (300, 3000),
    "Restaurants": (5, 100),
    "Gasoline": (1.0, 2.5),
    "Public Transport Pass": (20, 120),
    "Utilities": (50, 500),
    "Internet (60 Mbps)": (10, 70)
}

# Predefined weights for each category
WEIGHTS = {
    "Real Estate (€/m²)": 0.15,
    "Clothing": 0.10,
    "Groceries": 0.15,
    "Rent": 0.20,
    "Restaurants": 0.10,
    "Gasoline": 0.05,
    "Public Transport Pass": 0.10,
    "Utilities": 0.10,
    "Internet (60 Mbps)": 0.05
}


def fetch_prices(city: str, country: str) -> list:
    """
    Fetches raw cost of living price data for a given city and country.

    Args:
        city (str): City name.
        country (str): Country name.

    Returns:
        list: List of price entries from the API response.
    """
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"
    querystring = {"city_name": city, "country_name": country}
    headers = {
        "x-rapidapi-host": "cost-of-living-and-prices.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, verify=False)
        response.raise_for_status()
        return response.json().get("prices", [])
    except requests.RequestException as e:
        print(f"❌ Error fetching cost data: {e}")
        return []


def fetch_cost_details(city: str, country: str) -> list[dict]:
    """
    Organizes price data into categories with averages and detailed entries.

    Args:
        city (str): City name.
        country (str): Country name.

    Returns:
        list[dict]: List of categorized price data with averages.
    """
    prices = fetch_prices(city, country)
    detailed = []

    if not prices:
        print("⚠️ No prices loaded.")
        return []

    for category, ids in CATEGORIES.items():
        items = []
        for p in prices:
            try:
                good_id = int(p.get("good_id", -1))
                if good_id in ids and p.get("avg") is not None:
                    items.append({
                        "name": p.get("item_name"),
                        "price": round(p.get("avg"), 2),
                        "currency": p.get("currency", "") or "EUR"
                    })
            except Exception as e:
                print(f"❌ Error parsing product: {e}")

        if items:
            avg = round(sum(i["price"] for i in items) / len(items), 2)
            detailed.append({
                "category": category,
                "products": items,
                "average": avg
            })

    return detailed


def extract_and_normalize(prices: list) -> dict:
    """
    Extracts average prices per category and normalizes them to a 0–100 scale.

    Args:
        prices (list): Raw price data from the API.

    Returns:
        dict: Normalized scores per category.
    """
    results = {}

    for category, ids in CATEGORIES.items():
        values = [
            item["avg"] for item in prices
            if item.get("good_id") in ids and item.get("avg") is not None
        ]
        if values:
            avg_value = sum(values) / len(values)
            min_val, max_val = NORMALIZATION_RANGES.get(category, (0, 1))
            norm = min(max((max_val - avg_value) / (max_val - min_val) * 100, 0), 100)
            results[category] = round(norm, 2)
        else:
            results[category] = None

    return results


def calculate_weighted_score(normalized_data: dict) -> float:
    """
    Calculates the overall weighted cost score from normalized values.

    Args:
        normalized_data (dict): Category → normalized score.

    Returns:
        float: Weighted total score (higher = more affordable).
    """
    weighted_values = [
        value * WEIGHTS.get(category, 0)
        for category, value in normalized_data.items()
        if value is not None
    ]
    return round(sum(weighted_values), 2)


def get_normalized_cost_score(city: str, country: str) -> float | None:
    """
    High-level helper to fetch and score a city’s cost of living.

    Args:
        city (str): City name.
        country (str): Country name.

    Returns:
        float | None: Final cost score (0–100), or None if data is unavailable.
    """
    prices = fetch_prices(city, country)
    normalized_data = extract_and_normalize(prices)
    if not normalized_data:
        return None
    return calculate_weighted_score(normalized_data)
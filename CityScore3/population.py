"""
Population Lookup Module

Searches for cities by name and returns basic geographic and demographic information.

API used:
- GeoDB Cities API via RapidAPI: https://rapidapi.com/wirefreethought/api/geodb-cities
"""

import requests


def search_city_by_name(name_prefix: str, limit: int = 5):
    """
    Search for cities by name prefix and print population details.

    Args:
        name_prefix (str): Start of the city name (e.g., "berlin").
        limit (int): Maximum number of results to return (default: 5).

    Returns:
        None
    """
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {
        "namePrefix": name_prefix,
        "limit": str(limit),
        "sort": "-population"
    }

    headers = {
        "x-rapidapi-key": "ab8edca96cmshe86aae7faf8de8bp158d06jsn0db354d79061",
        "x-rapidapi-host": "wft-geo-db.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring, verify=False)

    if response.status_code == 200:
        data = response.json()
        print(f"🌍 Results for: '{name_prefix}'\n")
        for city in data["data"]:
            print(f"🏙️ {city['name']}, {city['country']}")
            print(f"  📍 ID: {city['id']}")
            print(f"  👥 Population: {city.get('population', 'Unknown')}")
            print(f"  🌐 Lat: {city['latitude']}, Lon: {city['longitude']}")
            print("-" * 40)
    else:
        print(f"❌ API error: {response.status_code}")
        print(response.text)


# 🔍 Example use
if __name__ == "__main__":
    search_city_by_name("berlin")
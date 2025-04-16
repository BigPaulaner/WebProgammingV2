"""
City Image Module

Downloads a city image from Unsplash and stores it locally.
Used for visually enhancing the result page background.

API used:
- Unsplash Image API: https://unsplash.com/documentation
"""

import os
import requests
from urllib.parse import quote


def download_city_background(city: str) -> str | None:
    """
    Downloads a city background image from Unsplash and stores it in the /static directory.

    Args:
        city (str): City name to search for on Unsplash.

    Returns:
        str | None: Relative URL to the saved image or None if download fails.
    """
    encoded = quote(city.lower())
    filename = f"city_photos/{encoded}.jpg"
    full_path = os.path.join("static", filename)

    if os.path.exists(full_path):
        return f"/static/{filename}"

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": "Client-ID K5UNzccA5Hdmt5iM41OgovwMCVQ1XJwYUlE3jFuQdS4"}
    params = {
        "query": city,
        "per_page": 1,
        "orientation": "landscape",
        "content_filter": "high"
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        results = res.json().get("results")
        if not results:
            return None

        img_url = results[0]["urls"]["regular"]
        img_data = requests.get(img_url).content

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(img_data)

        print(f"✅ Image saved as '{full_path}'")
        return f"/static/{filename}"

    except Exception as e:
        print(f"❌ Error downloading city image: {e}")
        return None
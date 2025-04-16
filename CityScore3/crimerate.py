"""
Crime Rate Module

Processes a static CSV file to calculate a normalized safety score per country.

Data source:
- `crime_data.csv`: A semicolon-separated file with country names and crime scores.

Note:
- Higher crime index = worse safety
- Safety score is inverted and normalized to a 0–100 scale
"""

import pandas as pd


def calculate_safety_score(filepath: str, country_name: str) -> float | None:
    """
    Calculate a country's safety score based on crime data from a CSV file.

    Args:
        filepath (str): Path to the crime data CSV file (semicolon-separated).
        country_name (str): Country to evaluate.

    Returns:
        float | None: Normalized safety score (0–100), or None if country not found or error occurs.
    """
    try:
        df = pd.read_csv(filepath, sep=';', names=["Country", "CrimeScore"], decimal=',', engine='python')
        df["Country"] = df["Country"].str.strip()

        match = df[df["Country"].str.lower() == country_name.lower()]
        if match.empty:
            return None

        value = match["CrimeScore"].values[0]

        # Normalize: lower crime score = higher safety
        min_val = 2
        max_val = 8
        normalized = (max_val - value) / (max_val - min_val) * 100

        return round(normalized, 2)

    except Exception as e:
        print(f"❌ Error processing crime data file: {e}")
        return None


if __name__ == "__main__":
    score = calculate_safety_score("crime_data.csv", "Colombia")
    print(f"🔐 Safety Score: {score} / 100" if score else "❌ Country not found or error.")
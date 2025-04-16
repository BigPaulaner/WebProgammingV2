"""
CityScore – City Comparison Web App

This module serves as the entry point of the CityScore3 project. It provides a Flask-based web interface 
that allows users to evaluate cities based on air quality, education, crime rate, healthcare, and 
cost of living. Scores are computed using multiple external APIs and datasets.

**Data sources and services used:**
- Geocoding: e.g. OpenCage, Nominatim
- Air Quality: OpenWeatherMap Air Pollution API
- Cost of Living: Numbeo API or similar
- Education: World Bank or equivalent sources
- Safety: Local crime dataset (CSV)
- Healthcare: WHO data or public APIs
- Weather: OpenWeatherMap API
- General info: Wikipedia API
"""

from flask import Flask, request, render_template
from geocoding import get_coordinates
from airpollution import get_normalized_air_quality, fetch_air_pollution_raw
from costofliving import get_normalized_cost_score, fetch_cost_details
from education import calculate_education_score
from crimerate import calculate_safety_score
from healthapi import calculate_health_score, fetch_health_details
from city_image import download_city_background
from wikipedia import get_wikipedia_summary
from currentweatherapi import fetch_weather_data

app = Flask(__name__)


def calculate_city_score(cost, air, edu, safety, health, weights):
    """
    Calculate the final weighted score for a city.

    Args:
        cost (float): Cost of living score.
        air (float): Air quality score.
        edu (float): Education score.
        safety (float): Safety/crime score.
        health (float): Healthcare score.
        weights (list of float): A list of 5 weights, each for one score. Should sum to 1.0.

    Returns:
        float or None: Final weighted score, or None if any component is missing.
    """
    components = [cost, air, edu, safety, health]
    if None in components:
        return None
    weighted_score = sum(v * w for v, w in zip(components, weights))
    return round(weighted_score, 2)


def get_country_name_from_code(code):
    """
    Convert a 3-letter ISO country code to a human-readable country name.

    Args:
        code (str): ISO3 country code, e.g. 'DEU', 'USA'.

    Returns:
        str or None: Country name, or None if code is unknown.
    """
    iso_to_name = {
        "DEU": "Germany", "FRA": "France", "USA": "United States", "GBR": "United Kingdom",
        "ESP": "Spain", "ITA": "Italy", "CAN": "Canada", "CHE": "Switzerland", "AUT": "Austria",
        "NLD": "Netherlands", "SVK": "Slovakia", "CZE": "Czech Republic", "POL": "Poland",
        "EUU": "European Union", "JPN": "Japan", "AUS": "Australia", "IND": "India", "BRA": "Brazil",
        "CHN": "China", "SGP": "Singapore", "DNK": "Denmark", "FIN": "Finland"
    }
    return iso_to_name.get(code.upper())


ISO_TO_COUNTRY = {
    "SGP": "Singapore", "DEU": "Germany", "FRA": "France", "USA": "United States", "CAN": "Canada",
    "ESP": "Spain", "ITA": "Italy", "NLD": "Netherlands", "CHE": "Switzerland", "AUT": "Austria",
    "BEL": "Belgium", "SWE": "Sweden", "NOR": "Norway", "DNK": "Denmark", "GBR": "United Kingdom",
    "JPN": "Japan", "KOR": "South Korea", "AUS": "Australia", "NZL": "New Zealand"
}


@app.route('/')
def home():
    """Render the homepage with the city input form."""
    return render_template('index.html')


@app.route('/score', methods=['POST'])
def score():
    """
    Handle form submission and calculate a city's overall score.

    Uses multiple data modules to fetch relevant data:
    - Coordinates
    - Air quality
    - Cost of living
    - Education
    - Safety
    - Healthcare

    Renders a results page with all individual scores and the final score.
    """
    city = request.form.get('city')
    country_code = request.form.get('country_code')
    country = request.form.get("country")

    if not city or not country_code or len(country_code) != 3:
        return render_template('result.html', error="❌ Please provide both city and a 3-letter country code (e.g. DEU).")

    country_name = get_country_name_from_code(country_code)
    if not country_name:
        return render_template('result.html', error="❌ Unsupported country code.")

    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return render_template('result.html', error="❌ Could not determine coordinates for this city.")

    air_score = get_normalized_air_quality(lat, lon)
    cost_score = get_normalized_cost_score(city, country_name)
    education_score = calculate_education_score(country_code)
    safety_score = calculate_safety_score("crime_data.csv", country_name)
    health_score = calculate_health_score(country_code)
    weather_data = fetch_weather_data(lat, lon)

    try:
        weights = [
            float(request.form.get('weight_cost', 0)),
            float(request.form.get('weight_air', 0)),
            float(request.form.get('weight_edu', 0)),
            float(request.form.get('weight_safety', 0)),
            float(request.form.get('weight_health', 0))
        ]
    except ValueError:
        return render_template('result.html', error="❌ Invalid weights entered.")

    if abs(sum(weights) - 1.0) > 0.01:
        return render_template('result.html', error="❌ Weights must add up to exactly 1.0.")

    if None in [air_score, cost_score, education_score, safety_score, health_score]:
        return render_template('result.html', error="❌ Failed to load one or more required data points.")

    final_score = calculate_city_score(
        cost=cost_score,
        air=air_score,
        edu=education_score,
        safety=safety_score,
        health=health_score,
        weights=weights
    )

    background_path = download_city_background(city) or "/static/default.jpg"
    wikipedia_summary = get_wikipedia_summary(city, lang="en")

    return render_template(
        "result.html",
        city=city,
        country=country,
        country_code=country_code,
        cost_score=cost_score,
        air_score=air_score,
        education_score=education_score,
        safety_score=safety_score,
        health_score=health_score,
        final_score=final_score,
        weights=weights,
        background_path=background_path,
        wikipedia_summary=wikipedia_summary,
        weather_data=weather_data
    )


@app.route("/details/cost")
def details_cost():
    """
    Render detailed cost of living information for a given city.
    """
    city = request.args.get("city")
    country_code = request.args.get("country")
    country_name = ISO_TO_COUNTRY.get(country_code.upper(), country_code)
    details = fetch_cost_details(city, country_name)
    return render_template("details_cost.html", city=city, country=country_name, details=details)


@app.route("/details/air")
def details_air():
    """
    Render detailed raw air pollution data for a given city.
    """
    city = request.args.get("city")
    country = request.args.get("country")
    lat, lon = get_coordinates(city)
    raw_data = fetch_air_pollution_raw(lat, lon)
    return render_template("details_air.html", city=city, country=country, data=raw_data)


@app.route("/details/education")
def details_education():
    """
    Render detailed education data for a given country.
    """
    country = request.args.get("country")
    details = fetch_education_details(country)
    return render_template("details_education.html", country=country, details=details)


@app.route("/details/safety")
def details_safety():
    """
    Render detailed safety/crime statistics for a given country.
    """
    country = request.args.get("country")
    value, normalized = get_safety_details("crime_data.csv", country)
    return render_template("details_safety.html", country=country, crime_value=value, score=normalized)


@app.route("/details/health")
def details_health():
    """
    Render detailed healthcare data for a given country.
    """
    country = request.args.get("country")
    details = fetch_health_details(country)
    return render_template("details_health.html", country=country, details=details)


if __name__ == '__main__':
    app.run(debug=True)
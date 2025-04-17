# 🧰 Frameworks and Libraries Used

This project leverages a small set of well-established Python frameworks and libraries to keep the stack lightweight, efficient, and easy to maintain.

---

## 🔧 Flask

> **Used for:** Web framework / backend routing

[Flask](https://flask.palletsprojects.com/) is a minimal and flexible Python web framework that allows for easy development of web applications.

✅ **Why Flask?**

- Lightweight and easy to set up
- Perfect for small- to mid-sized projects
- Allows full control over routing and rendering
- Easy integration with HTML templates and static assets

In this project, Flask handles:

- URL routing (`@app.route`)
- Form data processing
- Rendering templates via Jinja2

---

## 🔗 Requests

> **Used for:** Making HTTP requests to external APIs

[Requests](https://docs.python-requests.org/) is a user-friendly HTTP library for Python. It simplifies making calls to REST APIs.

✅ **Why Requests?**

- Human-readable and Pythonic syntax
- Built-in error handling
- Excellent community support

In this project, `requests` is used to interact with:

- OpenWeatherMap APIs
- Unsplash image API
- Wikipedia summary API
- World Bank and Cost of Living APIs (via RapidAPI)

---

## 📊 Pandas

> **Used for:** Handling and processing CSV data

[Pandas](https://pandas.pydata.org/) is the go-to library in Python for data analysis and manipulation.

✅ **Why Pandas?**

- Powerful and flexible DataFrame structures
- Simple CSV handling
- Ideal for filtering, cleaning, and aggregating data

Here, `pandas` is used to load and process crime statistics from a local CSV file (`crime_data.csv`), allowing us to extract and normalize scores for specific countries.

---

## 🌐 urllib3

> **Used for:** HTTP connection management (used indirectly through `requests`)

[urllib3](https://urllib3.readthedocs.io/) is a low-level HTTP client used by `requests` under the hood.

✅ **Why urllib3?**

While not used directly in this project, `urllib3` powers `requests` and also handles:

- HTTPS verification
- Connection pooling
- Retry strategies

In some modules (e.g. education and health), warnings from `urllib3` are explicitly disabled to avoid unnecessary output when calling APIs that may not support HTTPS verification fully.

---

## 📦 Summary

| Library   | Role                         | Reason for Use                                |
|-----------|------------------------------|------------------------------------------------|
| Flask     | Web backend / routing        | Lightweight, flexible, great for APIs + HTML   |
| Requests  | API communication            | Easy-to-use HTTP client                        |
| Pandas    | Data handling (CSV)          | Robust CSV parsing and filtering               |
| urllib3   | HTTPS / HTTP under the hood  | Connection handling (used via `requests`)      |
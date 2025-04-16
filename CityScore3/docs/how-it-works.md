# ⚙️ How Scoring and Weighting Works

CityScore3 uses a modular, weighted scoring system to evaluate and compare cities across five quality-of-life categories:

- Cost of Living, Air Quality, Education, Safety, Health

Each of these categories contributes to the **final City Score**, which is a single number between **0 (ideal)** and **100 (poor)**.

---

## 🧮 1. Normalization

Each category collects raw data from public APIs or datasets.

These raw values (e.g. air pollution in µg/m³, crime rates, literacy rates) are **normalized** to a common 0–100 scale:
This normalization ensures that completely different units (e.g. percent, prices, ratios) can be aggregated meaningfully.

## Normalization Examples

To better understand how normalization works in CityScore, here is real-world examples: one for a **negative metric** (lower is better) and one for a **positive metric** (higher is better).


### Example: Negative Metric – Air Pollution (PM2.5)

In this case, **lower values are better**. We normalize a PM2.5 air pollution value where:

- **0 µg/m³** is the best possible value
- **25 µg/m³** is considered the worst-case threshold
- The actual measured value is: **15 µg/m³**

**Formula:**

```text
normalized_score = (max - value) / (max - min) * 100

---

## ⚖️ 2. Weighting System
In CityScore3, users can assign **individual weights** to each quality-of-life category before calculating the final score for a city.
These weights determine **how much influence each category** should have on the overall result.
Users can assign a custom **weight** (from 0 to 1) to each category before submitting their city search.

> Example:
> - Cost of Living → 0.3
> - Air Quality → 0.2
> - Education → 0.2
> - Safety → 0.2
> - Health → 0.1

All weights must add up to **1.0**.

---

## 🔢 3. Final Score Calculation

Once all five category scores are normalized, the system applies the weighting:

```python
final_score = (
    cost_score   * weight_cost   +
    air_score    * weight_air    +
    education    * weight_edu    +
    safety_score * weight_safety +
    health_score * weight_health
)

---

## 🎯 4. Goal of the City Score

The final score represents a **quality-of-life index** where:

- **100** = worst-case value
- **0** = best possible value

Users can compare cities with a single number, while also exploring category-specific metrics in detail.

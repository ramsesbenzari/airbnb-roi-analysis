# Modelling Addendum

Extends `METHODOLOGY.md`. Three models, run after Phase 9.

**Rule for all three:** every model needs a stated question, a dumb baseline to beat, and an honest report of where it fails. A model without a baseline is unreadable — nobody knows if 0.72 is good.

---

## Model 1 — Nightly price

**Question:** What should a listing charge, and which listings are priced wrong?

### Setup

| Item | Choice |
|---|---|
| Type | Regression |
| Level | One row per listing |
| Target | `log(price)` |
| Split | 80/20, stratified by city |

**Use log price, not raw price.** Nightly prices are heavily skewed — a few luxury listings will dominate the errors otherwise. Convert back to real money when you report results.

### Features

| Group | Fields |
|---|---|
| Size | bedrooms, bathrooms, accommodates, beds |
| Type | property_type, room_type |
| Location | neighbourhood, latitude, longitude, distance to city centre |
| Rules | minimum_nights, instant_bookable, cancellation policy |
| Host | host_is_superhost, host listing count, years hosting |
| Quality | review scores (rating, cleanliness, location) |
| Amenities | total count, plus flags for pool, AC, wifi, parking, washer, kitchen |
| City | city as a category |

**Distance to centre** is worth the extra work. You have coordinates, so it's one calculation, and it usually ranks among the strongest features.

**Amenities** arrive as a messy text list. Parse it once, count them, and pull out 10–15 binary flags. This is the feature engineering step that makes the model actually good.

### Do not include

- Anything derived from your occupancy or revenue estimates
- `number_of_reviews` — it reflects how long the listing has existed, not its value
- `estimated_revenue` fields if Inside Airbnb supplies them

### Approach

1. **Baseline:** median price for that city and bedroom count. Write down its error.
2. **Linear regression** with the numeric and one-hot features. Interpretable, and sometimes surprisingly hard to beat.
3. **Gradient boosting** (LightGBM or XGBoost). Expect a solid improvement.
4. Compare all three in one table.

### Structural decision

Prices behave differently in each city — a pool matters in Marrakech and not in Amsterdam.

- **Recommended:** one global model with city as a feature, then 3–5 city-specific models as deep dives
- Global gives you scale and one clean number; the city models show you understand that markets differ
- Do not build 50 separate models

### Metrics

- MAE and RMSE on log scale
- Median percentage error in real currency — this is what you report to a non-technical reader
- R²

### The actual output

Not the prediction — the **residuals**.

- Listings priced far below prediction are underpriced
- Count them per city, look at what they have in common
- "In Lisbon, 14% of listings are priced at least 25% below what their features justify" is a finding. A model score is not.

---

## Model 2 — What drives bookings

**Question:** Which listing characteristics are associated with higher occupancy?

### The trap you must handle

Your occupancy estimate is **built from review counts**. So if you feed review counts into a model predicting occupancy, you are predicting the target using the target. The model will look excellent and mean nothing.

**Excluded, without exception:**
- `number_of_reviews`
- `number_of_reviews_ltm`
- `reviews_per_month`
- `last_review`, `first_review`
- Anything else that counts or dates reviews

Review **scores** (the 1–5 ratings) may stay — they measure quality, not volume. But note in your writeup that a listing needs reviews to have a score, so a mild link remains.

State this exclusion prominently. Spotting it yourself is exactly the kind of judgment that gets noticed in a review.

### Setup

| Item | Choice |
|---|---|
| Type | Regression |
| Target | Occupancy rate (nights booked ÷ nights available) |
| Level | Listing |
| Split | 80/20, stratified by city |

Use the **rate**, not raw nights. A listing available 60 days and a listing available 365 days aren't comparable on raw nights.

### Features

Same as Model 1, minus review counts, **plus nightly price** — price is a driver here, not the target.

### Approach

1. **Baseline:** city average occupancy for every listing
2. Linear regression
3. Gradient boosting
4. Feature importance, then SHAP values for the final model

SHAP is worth learning here. It shows direction, not just importance — "instant book raises occupancy by roughly X points" rather than "instant book is important." That's a sentence a business reader can use.

### Honesty requirement

Write this line, or your own version of it, in the report:

> This model shows association, not cause. Superhosts may get more bookings, or hosts with more bookings may become Superhosts. The data cannot separate the two.

Expect a modest R². That's normal — pricing is far more predictable than demand. Report it as it is. A weak result honestly reported reads better than an inflated one.

---

## Model 3 — City clustering

**Question:** What types of short-term rental market exist, and which cities belong to which?

### Setup

| Item | Choice |
|---|---|
| Type | Unsupervised |
| Level | One row per city (~50 rows) |
| Algorithm | K-Means, plus hierarchical (Ward) as a cross-check |

### The design decision that matters

**Cluster on the drivers. Then look at how ROI falls across the clusters.**

- If you cluster on ROI itself, you've just sorted cities by ROI with extra steps
- Clustering on drivers and *discovering* that one cluster carries most of the high-ROI cities is a genuine result

**Features to cluster on:**

| Feature | Why |
|---|---|
| Price per m² | Cost of entry |
| Median nightly rate | Revenue power |
| Estimated occupancy | Demand strength |
| Listings per 1,000 residents | Saturation |
| Share of listings held by multi-property hosts | Professionalisation |
| Tourism trend | Direction of travel |
| Regulation score (0–2) | Legal risk |

**Kept out of the clustering, then compared against it:** ROI.

### Steps

1. **Scale every feature.** K-Means measures distance — without scaling, price per m² swamps everything else. StandardScaler.
2. Check correlations. Drop one of any near-duplicate pair.
3. Choose k using the elbow chart and silhouette score together. With 50 cities expect k between 3 and 5.
4. Run K-Means. Then run hierarchical clustering separately.
5. **If both methods group the cities roughly the same way, your clusters are real.** If they disagree badly, the structure isn't there — say so.
6. PCA down to 2 dimensions purely for the scatter chart.

### The deliverable

**Name the clusters in plain language.** This is the entire value of the exercise.

Something like:
- Cheap entry, strong demand, light regulation
- Expensive, stable, mature
- Saturated and legally hostile
- Thin market, low demand

Then a table: cluster, cities in it, average ROI, average risk. That one table is worth more than every metric in this document.

---

## Repo additions

```
notebooks/
  11_model_price.ipynb
  12_model_occupancy.ipynb
  13_cluster_cities.ipynb
src/
  features.py        # amenity parsing, distance to centre, shared feature build
  evaluate.py        # baseline comparison, metric table
models/
  *.pkl
reports/
  model_card.md
```

**`features.py` matters.** Models 1 and 2 share almost all their features. Build them once. Copy-pasting the feature block between two notebooks is the thing reviewers notice.

**`model_card.md`** — one page per model: question, data, features, what was excluded and why, baseline, results, known weaknesses.

---

## Order of work

| Step | Work |
|---|---|
| 11 | Feature engineering — amenities, distance, cleanup |
| 12 | Price model: baseline → linear → boosted → residual analysis |
| 13 | Occupancy model: exclusions → baseline → boosted → SHAP |
| 14 | Clustering: scale → k selection → two methods → naming |
| 15 | Model cards, then fold findings into the main README |

Step 11 will take longer than steps 12 and 13 combined. That's normal and it's where the model quality actually comes from.

---

## Three things that will sink this

1. **Leakage in Model 2.** Review counts in the features. Covered above — this is the one to get right.
2. **No baseline.** An R² with nothing to compare it to tells the reader nothing.
3. **Models with no question.** Each model above answers something a property investor would ask. Keep it that way.

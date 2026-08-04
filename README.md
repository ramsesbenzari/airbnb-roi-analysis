# Short-Term Rental ROI — Which Cities Actually Pay Off

Analysis of Airbnb listing data and property prices across 15 major short-term rental markets, estimating the return on buying a property to rent nightly — and checking whether it's even legal to do so.

**Status:** in progress

---

## Headline findings

<!-- WRITE THIS LAST. Three to five bullets, plain language, numbers included.
     A reader should be able to stop here and still know what you found.
     Example shape:
     - City X leads on raw return at Y%, but sits under a night cap that removes most of it
     - The top of the ranking is driven by cheap property, not high nightly rates
     - N of the top 10 markets are legally restricted -->

_To come._

---

## The question

Given a fixed budget to buy an apartment and rent it nightly, which city gives the best return?

Sub-questions:
1. Which cities have the highest estimated net yearly ROI?
2. Is that driven by cheap property or strong nightly rates?
3. Where does regulation cap or kill the opportunity?
4. How crowded is each market already?
5. How much does the ranking move if the assumptions are wrong?

---

## Results

### ROI ranking

<!-- Table: city, country, ROI %, payback years, regulation status, saturation -->

_To come._

### What drives the returns

<!-- The price-vs-property-cost scatter and what it shows -->

_To come._

### Regulation

<!-- The cities where the numbers and the law disagree -->

_To come._

### How stable is this ranking

<!-- Rank across sensitivity scenarios -->

_To come._

---

## Modelling

### Nightly price model

<!-- Baseline vs linear vs boosted, error in real money, and the residual finding -->

_To come._

---

## How the cities were chosen

No cities were hand-picked. The sample is the result of a filter:

1. Every city published by Inside Airbnb with a snapshot in the last 12 months
2. At least 500 active entire-home listings
3. A property price per m² available from Numbeo
4. Of those that passed, the 15 largest by active listing count

| Filter step | Cities remaining |
|---|---|
| Starting list | |
| Recent snapshot | |
| 500+ entire homes | |
| Price data available | |
| Top 15 by size | 15 |

**Final sample:**

<!-- City, country, snapshot date, listings after cleaning -->

---

## Method in brief

Full detail in [METHODOLOGY.md](METHODOLOGY.md) and [MODELLING.md](MODELLING.md).

- Occupancy is **estimated**, not measured — Airbnb publishes no booking data. Estimated from review volume, then validated against Eurostat's platform booking figures for three European cities.
- Revenue = estimated nights booked × median nightly rate
- Costs = platform fee, utilities, maintenance, insurance
- Property cost = price per m² × assumed unit size, plus buying fees and furnishing
- ROI = net yearly revenue ÷ total property cost

---

## Assumptions

Every made-up number in this project, in one place.

| # | Assumption | Value | Basis | Confidence |
|---|---|---|---|---|
| 1 | Review rate | 0.50 | Convention, tuned against Eurostat | Low |
| 2 | Average stay | 3 nights | Fallback default | Low |
| 3 | 1BR size | 50 m² | Estimate | Medium |
| 4 | 2BR size | 75 m² | Estimate | Medium |
| 5 | Buying costs | 8% of price | Rough global average | Medium |
| 6 | Utilities | 8% of revenue | Estimate | Low |
| 7 | Maintenance | 1% of value/yr | Standard property rule | High |
| 8 | Occupancy ceiling | 70% | Data sanity limit | High |
| 9 | Reporting currency | USD, rates pinned 2026-08-04 | — | High |
| 10 | Management | Self-managed base case | — | High |

Everything marked Low confidence is tested in the sensitivity check.

---

## Limitations

1. Occupancy is modelled from review counts, not measured
2. Nightly price is the advertised rate — it excludes cleaning and service fees
3. Property prices are crowdsourced and city-average, missing neighbourhood variation
4. Taxes are excluded and vary enormously by country
5. 15 markets, not the world
6. One snapshot — no seasonality, no trend
7. Regulation changes faster than this analysis will be updated

---

## Data sources

| Source | Used for |
|---|---|
| Inside Airbnb | Listings, nightly price, availability, reviews |
| Numbeo | Property price per m² |
| Eurostat | Platform booking data, used to validate the occupancy estimate |
| Manual research | Short-term rental regulation per city |

---

## Repo

```
data/raw/          Untouched downloads (gitignored)
data/processed/    Cleaned tables
notebooks/         Analysis, numbered by phase
src/               Shared functions
reports/           Model cards
```

## Running it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Run the notebooks in numbered order.

---

## Stack

Python, pandas, DuckDB, scikit-learn, LightGBM, plotly

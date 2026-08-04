# Short-Term Rental ROI — Scope & Methodology

**Question:** Among the world's major short-term rental markets, which cities offer the best return on investment for buying a property and renting it on Airbnb?

**Status:** Scope locked before analysis begins. Any change to the rules below gets logged in the changelog at the bottom.

---

## 1. Business questions

1. Which cities have the highest estimated net yearly ROI?
2. Is high ROI driven by cheap property or by strong nightly rates?
3. Where does local regulation cap, ban, or threaten the opportunity?
4. How crowded is each market already?
5. How much does the ranking change if my assumptions are wrong?

Question 5 is the one that separates this from a generic ranking. Do not skip it.

---

## 2. Scope boundaries

| In scope | Out of scope |
|---|---|
| Entire homes and apartments | Private rooms, shared rooms, hotel listings |
| 1 and 2 bedroom units | Studios, 3+ bedrooms, villas |
| Listings active in the last 12 months | Dormant and ghost listings |
| Cash purchase | Mortgages, leverage, financing costs |
| One yearly snapshot | Month-by-month seasonality |
| Property price, furnishing, buying fees | Income tax, property tax, capital gains |
| City-level averages | Neighborhood-level analysis |

Everything in the right column goes in the limitations section, not in the bin. Naming what you left out is part of the deliverable.

---

## 3. Data sources

| Source | Gives you | Level | Cost | Main weakness |
|---|---|---|---|---|
| Inside Airbnb | Listings, nightly price, availability, reviews, room type | Listing | Free | No real bookings or revenue |
| Inside Airbnb country archives | Whole-country coverage for 12 countries | Listing | Free | Only 12 countries |
| Numbeo | Price per m², city centre and outside | City | Free pages / paid API | Crowdsourced, thin in small cities |
| National statistics offices | Official property prices | Varies | Free | Different definitions per country, hard to combine |
| Manual research | Short-term rental rules per city | City | Time | Changes fast, needs a "checked on" date |
| Exchange rate source | Currency conversion | Daily | Free | Must pin one date, not live |

**Check the Inside Airbnb data dictionary before you start.** Recent releases have added estimated occupancy and revenue fields. If those exist in your files, do not use them as your answer — build your own estimate and use theirs as a cross-check. Two independent estimates agreeing is a strong result. Disagreeing is an interesting finding.

---

## 4. City selection rule

Written as a filter so nobody can accuse you of cherry-picking.

1. Start from every city Inside Airbnb publishes
2. Keep cities with a snapshot dated within the last 12 months
3. Keep cities with at least 500 active entire-home listings
4. Keep cities with a Numbeo price per m² backed by enough contributors
5. Whatever survives is the sample

**Rules of the rule:**
- No country quotas. If Spain contributes six cities, that is the correct answer, not a problem to fix.
- If the filter yields 43 or 61 cities, take that number. Do not pad to reach 50.
- Record how many cities each filter step removed. That table goes in the report.

For the 12 archive countries you can rank every covered city, so you can actually check whether the famous city is the best one in its country. Everywhere else, you are limited to what is published — say so.

---

## 5. Methodology

### 5.1 Cleaning

- Keep `room_type = "Entire home/apt"`
- Keep `bedrooms` in (1, 2)
- Drop listings with zero reviews in the last 12 months
- Drop listings with a null or zero nightly price
- Remove the top and bottom 1% of nightly prices per city (kills luxury outliers and data errors)
- Convert all prices to a single currency using one pinned exchange-rate date
- One row per listing per city snapshot. Deduplicate on listing id.

### 5.2 Occupancy estimate

Inside Airbnb gives no bookings, so occupancy is modelled:

```
estimated nights booked per year
  = reviews in last 12 months
  × (1 / review rate)
  × average length of stay
```

Then capped twice:
- Cannot exceed `availability_365` (you cannot book a night the host blocked)
- Cannot exceed the city's legal night limit where one exists

**Parameters:**

| Parameter | Base value | Why |
|---|---|---|
| Review rate | 0.50 | Roughly half of stays leave a review. Common assumption in this field. |
| Average length of stay | 3 nights | Use a city-specific value where you can find one; 3 is the fallback |
| Hard occupancy ceiling | 70% | Above this is almost always a data error, not a real business |

This estimate is the single biggest source of error in the whole project. Say that out loud in the report.

### 5.3 Revenue

```
gross yearly revenue = estimated nights booked × median nightly price
```

Use **median** nightly price per city, not mean. The mean gets dragged by penthouses.

**Known gap:** the Inside Airbnb price field is the advertised nightly rate. It excludes cleaning fees and platform service fees, and it is what the host asks, not what guests paid. Your revenue figure is therefore approximate and probably slightly low. Document it.

### 5.4 Operating costs

Subtract from gross revenue:

| Cost | Base value |
|---|---|
| Platform host fee | 3% of revenue |
| Cleaning | Assume passed to guest, so 0 |
| Utilities, internet, supplies | 8% of revenue |
| Maintenance and repairs | 1% of property value per year |
| Insurance | 0.5% of property value per year |
| Property management | 0% (self-managed base case, 18% in the alternate scenario) |
| Vacancy | Already captured in the occupancy estimate — do not double count |

### 5.5 Property cost

```
total property cost
  = (price per m² × assumed size)
  + buying costs
  + furnishing
```

| Input | Base value |
|---|---|
| 1-bedroom size | 50 m² |
| 2-bedroom size | 75 m² |
| Buying costs (notary, transfer tax, agent) | 8% of purchase price |
| Furnishing and setup | Flat amount, scaled to local cost of living |

Use the **city centre** price per m². Short-term rentals live in central areas; using the outside-centre price would flatter your ROI.

### 5.6 ROI

```
net yearly ROI = (gross revenue − operating costs) ÷ total property cost
```

Report it as a percentage. Also report the payback period in years (1 ÷ ROI) — it is more intuitive for readers.

### 5.7 Regulation layer

A manual table, one row per city in the sample:

- Are short-term rentals allowed?
- Is there a night cap per year?
- Is a licence or registration required?
- Is there a moratorium or announced ban?
- Source link and date you checked

Then classify each city: **Open / Restricted / Hostile**.

A city that tops the ROI ranking but sits in Hostile is the most interesting finding in your whole report. Lead with it.

### 5.8 Market saturation

Simple and cheap:

- Active listings per 1,000 residents
- Share of listings held by hosts with 3 or more properties

High saturation plus high ROI means the number is unlikely to survive your entry.

### 5.9 Sensitivity check

Rerun the ranking under each of these and see whether your top 10 holds:

| Scenario | Change |
|---|---|
| Pessimistic reviews | Review rate 0.30 |
| Optimistic reviews | Review rate 0.70 |
| Longer stays | Average stay 5 nights |
| Managed property | Add 18% management fee |
| Expensive entry | Buying costs 12% |

Output: a table showing each city's rank in every scenario. Cities that stay in the top 10 across all of them are your real answer. Cities that swing wildly are a warning, and that is a finding worth writing up.

---

## 6. Assumptions register

Every made-up number in one table, with its value and where it came from. This lives in the README, not buried in a notebook.

| # | Assumption | Value | Basis | Confidence |
|---|---|---|---|---|
| 1 | Review rate | 0.50 | Industry convention | Low |
| 2 | Average stay | 3 nights | Fallback default | Low |
| 3 | 1BR size | 50 m² | Estimate | Medium |
| 4 | 2BR size | 75 m² | Estimate | Medium |
| 5 | Buying costs | 8% | Global rough average | Medium |
| 6 | Utilities share | 8% of revenue | Estimate | Low |
| 7 | Maintenance | 1% of value/yr | Standard property rule | High |
| 8 | Occupancy ceiling | 70% | Data sanity limit | High |
| 9 | Exchange rates | Pinned date | Published rate | High |

Anything marked Low confidence must appear in the sensitivity check.

---

## 7. Limitations

State these plainly in the report:

1. Occupancy is estimated from review counts, not measured
2. Nightly price is advertised, not realised, and excludes fees
3. Property prices are crowdsourced and city-average, so they miss neighborhood variation
4. Taxes are excluded and they differ enormously by country
5. Sample is 50-ish published markets, not the world
6. One snapshot in time — no seasonality, no trend
7. Regulation changes faster than this report will be updated

---

## 8. Deliverables

- `README.md` — findings first, then method summary, then assumptions register
- `notebooks/` — numbered notebooks, one per phase, clean outputs
- `data/raw/` — untouched downloads, never edited
- `data/processed/` — cleaned outputs
- `src/` — reusable functions, not copy-pasted cells
- `regulation.csv` — the manual research table
- Final ranking table and 5 to 6 charts

Charts worth building:
- ROI ranking, coloured by regulation status
- Nightly price vs. property price scatter, to show what drives ROI
- Rank stability across sensitivity scenarios
- Saturation vs. ROI

---

## 9. Phases

| Phase | Work | Output |
|---|---|---|
| 1 | Apply city filter, download files, load raw | City list with filter drop-off table |
| 2 | Clean and standardise, convert currency | Clean listing table |
| 3 | Build and validate occupancy estimate | Occupancy per city |
| 4 | Revenue and cost model | Net revenue per city |
| 5 | Property price and total cost | Total cost per city |
| 6 | Compute ROI, first ranking | Draft ranking |
| 7 | Regulation research | `regulation.csv` |
| 8 | Saturation metrics | Saturation per city |
| 9 | Sensitivity scenarios | Rank stability table |
| 10 | Charts and writeup | Final README |

Phase 3 is the hard one. Budget more time for it than feels reasonable.

---

## 10. Stack

- Python with pandas for loading and cleaning
- DuckDB for all aggregation and joins — SQL directly on your files, no server
- plotly or matplotlib for charts
- Jupyter for the analysis, exported clean

Writing the aggregation in SQL rather than pandas is deliberate: it doubles as SQL practice on genuinely messy data.

---

## 11. Open decisions

Decide these before Phase 1:

- **Reporting currency** — USD or EUR
- **Exchange rate date** — pin one and never change it
- **Base case management** — self-managed or professionally managed
- **Furnishing amount** — flat global figure or scaled to local costs
- **Tie-break rule** — when two cities land within 0.5% ROI of each other

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| — | Added modelling phase, see `MODELLING.md` | Three models added: nightly price, booking drivers, city clustering |

**Impact on scope above:** the cleaned listing-level table is now a required deliverable, not an intermediate step. Save it to `data/processed/` as parquet. The models depend on it.

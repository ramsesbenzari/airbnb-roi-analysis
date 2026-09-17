# Methodology

Supporting detail for the analysis in [README.md](README.md). The README carries the findings and the limitations; this file records the decisions behind them, and what was deliberately left out.

---

## The question

For each city: if you bought a 1–2 bedroom apartment and let it short-term on Airbnb, what annual return would you get?

Four things follow from that phrasing:

- **Buying, not letting what you already own.** Property cost sits in the denominator. This is why revenue-ranked market reports answer a different question — useful to an existing owner, misleading to a buyer.
- **1–2 bedrooms.** A size the cost side can price consistently. Inside Airbnb publishes two files per city: a summary file of 16 columns with no bedroom count, and a detailed file of 75 columns that includes one. The first pass used the summary files; enforcing the bedroom filter meant downloading the detailed set for every surviving city.
- **Entire homes.** Private rooms are a different product with different economics.
- **Annual.** Occupancy covers twelve months, not a peak season.

---

## The equation

```
revenue     = median nightly price (1-2 bed entire homes, USD) × estimated nights booked
utilities   = Numbeo monthly utilities × 12, scaled to apartment size
maintenance = 1% of property value per year
value       = Numbeo price per m² × apartment size

ROI = (revenue − utilities − maintenance) ÷ value
```

Computed twice per city — once with Numbeo's centre price, once with outside-centre — and reported as a range. Averaging the two would blend a cheap suburb with an expensive core, while Airbnb revenue concentrates centrally.

Three things fall out of the algebra, each worth knowing before reading the results:

- **Apartment size survives in one term only** — revenue over value. It cancels out of utilities and maintenance entirely.
- **Maintenance collapses to a flat 1 percentage point** for every city, so it shifts all results equally and changes no rankings.
- **Utilities are independent of the size assumption**, because scaling Numbeo's 85 m² quote down to the assumed size and then dividing by that same size cancels.

### Excluded from the model

| Excluded | Why |
|---|---|
| Lodging and income taxes | Vary by jurisdiction and were not researched per city. Chicago alone carries 27.75% on lodging. |
| Regulation | No consolidated cross-city source. Decisive in several markets — see README. |
| Financing | Depends on the buyer, not the city. |
| Management fees | Depends on whether the owner self-manages. |
| Furnishing, insurance, cleaning | Not available per city from any consistent source. Their size relative to the modelled terms was not measured. |

---

## Decisions taken during the analysis

**Cities, not regions.** The test applied was practical rather than administrative: do the Airbnb file and the Numbeo entry describe the same housing market? Metro-level files were kept, because Numbeo prices metros. Regional files were dropped, because a region contains many separate housing markets and no single price per m² describes it.

**A range rather than a single ROI.** The gap between a city's centre and outside-centre return is often wider than the gap between cities. Collapsing it to one number would hide the larger effect.

**Median rather than mean for every city-level figure.** Prices are right-skewed with extreme outliers — Buenos Aires runs to 171 million pesos. The median resists that; the mean does not. Means appear only where the input is already a per-city summary, such as the average centre-to-outside gap by country.

**Prices trimmed to each city's 1st–99th percentile before any median is taken.** The trim changes almost nothing on its own, since medians already resist outliers. Its value is positional: sitting upstream of both the price and occupancy medians, it guarantees they are computed over the same listings.

**Occupancy from review counts, not availability.** `availability_365` is forward-looking while review counts are backward-looking, and an unavailable listing is not the same as a booked one — a host who blocks the calendar looks identical to one booked solid.

**Costs limited to utilities and maintenance.** Both are available per city from a single consistent source. Estimates that vary by buyer rather than by city would add noise without adding information.

---

## What the correlations do and do not say

The README reports correlations between each input and ROI. Two notes on reading them.

**A weak correlation is not the same as an unimportant variable.** Property price scores −0.36, which understates its role. For any single city it is decisive: halve the purchase price and the return doubles.

The weakness shows up only when comparing cities, which is the only thing a correlation can measure — a single city gives one price and one return, with nothing to correlate. Every correlation in this project is therefore a statement about the 80 cities compared against each other, never about what happens inside one of them.

And when comparing cities, a high property price signals two opposite things at once:

| What a high price tells you | Effect on return |
|---|---|
| The flat costs more to buy | lower |
| The city is expensive generally, so nightly rates are higher | higher |

The two partly cancel, so knowing a city's property price leaves you little wiser about its return. That is a statement about price as a clue, not about price as a cause.

**Occupancy scores highest because it has no such conflict.** It correlates −0.20 with property price, so busy cities tend also to be cheap ones. High occupancy and low cost arrive together and both raise the return.

---

## Reproducibility

Every input is free and public. The pipeline runs end to end from a clone:

1. `get_links.py` — scrapes Inside Airbnb download URLs
2. `download.py` — fetches the city files
3. `01_profile_data.ipynb` — profiles the raw data
4. `02_cleaning_and_analysis.ipynb` — builds the `cities` and `city_metrics` tables, exports `results.csv`
5. `03_charts.ipynb` — produces the figures, including maps drawn with GeoPandas against Natural Earth country outlines

City coordinates for the maps are the median latitude and longitude of each city's listings, taken from the Inside Airbnb files rather than a separate geocoding source. All maps share one colour scale fixed at −1% to 12%, so a given colour means the same return on each of them.

The three Numbeo tables were exported by hand and committed, since Numbeo has no export API. Exchange rates are pinned to 2026-06-30 so results do not drift with currency movements.

---

## Not done

Recorded so the scope is explicit rather than implied:

- **A regulation layer** for the top 20 cities — legality, night caps, primary-residence requirements, registration costs. This is the single most valuable addition the analysis lacks.
- **Tax rates** for the top 20, lodging and income.
- **City-level apartment sizes**, should a consistent cross-country source appear.
- **A comparison against long-term letting**, using Numbeo's gross rental yield column.
- **Markets Inside Airbnb does not cover**, scraped directly and run through the same pipeline rather than imported from a source with different methodology. Countries like Morocco, Egypt, India and Indonesia have no coverage at all.

  Coverage is also uneven within the countries that do appear. The United States contributes 21 cities; Japan, Turkey, Mexico, Hungary and a dozen others contribute one each. France has three. That imbalance is not a judgement about which markets matter — it reflects where Inside Airbnb has volunteers. The 80 cities are the ones that happen to be maintained, not a designed sample, and no country in the set has all of its significant markets represented.
- **Modelling.** Nightly price prediction, occupancy drivers and city clustering were scoped but not built. They are a separate project using this dataset as input.

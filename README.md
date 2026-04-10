# Ontario Energy Market Analytics — IESO Public Data
**Tools:** Python (Pandas, NumPy, matplotlib) · Power BI · Excel
**Data Source:** IESO Public Reports
**Study Window:** December 2025 – January 2026

## Project Overview

Independent analytical study of Ontario's wholesale electricity market using publicly available IESO data. Built to develop analytical intuition about how Ontario demand, Day-Ahead prices, and Real-Time prices interact — and to identify conditions under which the market enters stress or spike regimes.

Implemented across two platforms:
- **Power BI** — interactive dashboards for visual exploration and stakeholder reporting
- **Python (Pandas, NumPy, matplotlib)** — data pipelines, validation, anomaly detection, and independent verification

## Dashboards Built

### 1 — Ontario Hourly Demand and Day-Ahead Price
Window: Dec 28 – Jan 3 | Hour convention: HE (Hour Ending)

- Demand follows a consistent daily shape: overnight low → morning ramp → evening peak (~HE18 / 5 PM)
- Price broadly tracks demand but diverges during marginal constraint conditions
- Dec 28: low demand day with HE1 price spike — markets price the marginal condition, not the average
- Largest intraday demand swing: Dec 29 (~5,010 MW range)

### 2 — Price Spike Explorer: Spike Premium Quantification

Three spike definitions (threshold, top-N, percentile) and two baselines (rolling 24h average, same-hour 7-day average).

- Demand alone does not explain the largest price moves — several high-premium spikes occurred with demand in a narrow 18.8–20.7 GW band, consistent with constraint/scarcity behaviour
- Baseline choice changes the story: one 5 PM event showed +$170/MWh vs rolling 24h, and +$200/MWh vs same-hour 7-day average
- Spikes differ in duration: flash spikes (~2 hours) vs persistent stress (~5–6 hours) have very different risk profiles
- Timing is not random: spikes cluster around weekday ramp and peak hours

### 3 — Spike Frequency and Distribution Analysis

- Spike frequency: 8.46% of all hours in the Dec–Jan window
- Average spike premium: $43.04/MWh
- 90th percentile: $70.65/MWh | 95th percentile: $83.83/MWh
- 44 spike hours in $0–$50 range; 21 hours above $50/MWh; 2 hours above $100/MWh
- Spikes cluster most heavily around HE18 (5 PM evening peak)
- Weekends showed more spike hours than weekdays — pointing to supply/constraints as key drivers beyond demand volume

### 4 — Day-Ahead vs Real-Time Price Divergence
Window: Jan 17 – Jan 31, 2026 (winter storm period)

- Divergence clusters on specific days — Jan 24–29 showed the largest absolute spreads
- Extreme event: Jan 24, 2026 ~8 AM — DA: $259.35/MWh, RT: $1,327.41/MWh
- Separates "DA already saw stress" from "stress emerged only in Real-Time"

### 5 — DA vs RT Surprise Hours: Winter Storm Deep Dive

- Divergence is event-driven, not a persistent drift — large deviations concentrate in Jan 24–29
- A small number of tail hours drive most of the total absolute spread
- Surprise hours frequently occur during system transition periods (morning ramp / late-day changes)
- Post-event: large negative spreads on Jan 26 and 28 suggest DA remained priced for stress while RT relaxed faster — consistent with post-event risk premium normalization

Illustrative event:
- Date: Jan 24, 2026 ~8:00 AM
- DA Price: $259.35/MWh
- RT Price: $1,327.41/MWh
- Ontario Demand: ~20 GW
- Market Demand: ~22.4 GW

## Skills Demonstrated

- End-to-end data pipeline development in Python
- Time-series analysis and statistical anomaly detection
- Data quality validation and QA/QC
- Power BI dashboard development for stakeholder reporting
- Cross-validation of findings across Python and Power BI
- Structured analytical reporting with methodology and implications

## Data Sources

All data from IESO public reports: http://reports.ieso.ca/public/
- Demand: PUB_Demand hourly CSV
- Day-Ahead Price: PUB_DAOntarioZonalPrice XML
- Real-Time Price: PUB_RealTimeIDCPrice XML

## About

Built independently as part of professional development targeting Ontario energy market and infrastructure analytics roles.

**Author:** Karan Patel
**LinkedIn:** linkedin.com/in/karan-patel-eit
**Email:** karanpatelias@gmail.com

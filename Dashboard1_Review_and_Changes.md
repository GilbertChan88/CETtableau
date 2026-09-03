# Dashboard 1 (Total Web Traffic) — Review & Changes

This document reviews the existing `Web Traffic Analysis.twb` attempt against the client
requirement `Dashboard 1 - Webtraffic.png`, and describes the improvements that were added.
**No original sheets or dashboards were deleted** — all additions are new and prefixed with `D1 |`.

---

## 1. What the client asked for (Dashboard 1 — "Total Web Traffic")

| Requirement | Detail |
|---|---|
| Filters (single/multi-select) | Campaign ID, Campaign Name, Duration (start–end date), Department/School/Institute |
| Graph 1 | Traffic over time for **all** CET pages |
| Graph 2 | Traffic over time for **selected** pages |
| Key Metrics panel | Page Name, Total Page Views, Total Unique Users, Average Session Duration |
| Example (nice-to-have) | Weekly line of Total Page Views with the **campaign period shaded**, spike annotations, and colour blocks for ads during the campaign |

## 2. Data model note

The traffic data (`Mock_WebTraffic.csv`) and the campaign master join on **`Campaign Name for UTM`**.
The workbook already contains a datasource — **`Web Traffic Analysis`** — that performs this join and
exposes everything Dashboard 1 needs: `Date`, `Page path and screen class`, `Views`, `Total users`,
`Sessions`, `Average session duration`, plus `Campaign ID`, `Campaign Name`, `Dept/Sch/Institute`,
`Start Date` and `End Date`. All new work was built on this single datasource.

## 3. Review of the original attempt

Strengths:
- The `Web Traffic Analysis` datasource correctly joins traffic to campaigns on `Campaign Name for UTM`.
- The `True Avg Session Duration` calc — `SUM([Average session duration]*[Sessions]) / SUM([Sessions])`
  — is a properly **weighted** average (a simple `AVG` would be misleading). Good.
- `Traffic Trend Analysis (v2)` already proved that a **campaign-period reference band**
  (from `Start Date` to `End Date`) is feasible — this answers the client's open question.

Gaps / issues identified:
1. **No single consolidated Dashboard 1.** The pieces were spread across several dashboards
   (`Web Traffic & Campaign Dashboard`, `... (v0.2)`, `Web Traffic Dashboard`).
2. **Two different datasources were mixed** (`Web Traffic Analysis` vs `Mock + Live Data`). Because
   dashboard filters are datasource-scoped, filters could not act on every chart at once.
3. **Graph 1 vs Graph 2 were not separated** — there was no distinct "all pages" vs "selected pages" view.
4. The `Traffic Trend` sheet carried a **huge hard-coded "Keep Only" page filter** listing hundreds of
   individual page URLs. This is fragile and silently drops any new/renamed page.
5. **Filters were hard-coded to specific members** instead of open `All`-member filters, so they did not
   behave as reusable interactive controls.
6. **No clean Key-Metrics table** containing exactly the four requested fields.
7. The campaign-period shading existed only in a `Mock + Live Data` sheet, not integrated with the
   main traffic view.

## 4. What was added (all new — originals untouched)

### New calculated field (on `Web Traffic Analysis`)
- **`In Campaign Period`** (boolean): `[Date] >= [Start Date] AND [Date] <= [End Date]`.
  Useful for shading / for the future "ad colour blocks" idea.

### New worksheets
1. **`D1 | Traffic - All CET Pages`** — *Graph 1*.
   Weekly (`WEEK(Date)`) line of **Total Page Views** and **Total Unique Users** across all pages, with a
   shaded **campaign-period reference band** built from `Start Date` → `End Date`. Filters are open
   (`All` members) so they act as interactive controls: Campaign ID, Campaign Name, Department.
2. **`D1 | Traffic - Selected Pages`** — *Graph 2*.
   Weekly line of **Total Page Views**, one coloured line **per page**, driven by a `Page path` filter
   so the user can pick specific page(s) to compare. Same campaign/department filters.
3. **`D1 | Key Metrics`** — *Key Metrics panel*.
   A per-page table: **Page** (row) × **Total Page Views**, **Total Unique Users**,
   **Average Session Duration** (weighted), sorted by Views. The hard-coded page list was removed.

### New dashboard
- **`Dashboard 1 - Total Web Traffic`** assembling, top to bottom:
  1. Title "Total Web Traffic".
  2. Filter row: **Campaign ID, Campaign Name, Department, Duration (Date range slider)**.
  3. Graph 1 (All CET Pages) with the shaded campaign period.
  4. A **Page** filter control.
  5. Graph 2 (Selected Pages).
  6. Key Metrics table.

The `Duration (Date range)` control uses the workbook's existing datasource-level (`shared-views`)
date filter on `Web Traffic Analysis`, so it applies consistently across the D1 sheets — the same
mechanism the original dashboards relied on.

## 5. Recommended manual follow-ups in Tableau Desktop

These are quick clicks that are best done in the Tableau UI (they cannot be reliably hand-authored):
- **Make the filters global:** right-click each filter on the dashboard → *Apply to Worksheets →
  All Using This Data Source*, so Campaign ID / Name / Department / Date control all three D1 sheets.
- **Change filter display:** set Campaign ID / Name / Department to *Multiple Values (dropdown)* and
  the Date filter to a *Range of Dates* slider if not already shown that way.
- Optionally add **mark labels/annotations** on Graph 1 to call out spikes (as in the client example),
  and format the Average Session Duration column as `mm:ss`.
- Optionally add the "different ads during campaign period" colour blocks by layering a Gantt bar
  (see the original `Traffic Trend V3` for a starting pattern) keyed on `Marketing Channel`.

## 6. Validation
- The workbook XML was checked and is **well-formed** after every edit.
- All 12 original worksheets and all 4 original dashboards remain unchanged; only additions were made.


## 7. Update — Date-axis alignment & date-filter sync (Graph 1 ↔ Graph 2)

**Goal:** the dashboard Date (Duration) filter should update *both* time-series charts together, and
the two charts should share the same week/date axis so they line up when stacked.

**Date filter sync (both graphs):**
Both `D1 | Traffic - All CET Pages` and `D1 | Traffic - Selected Pages` sit on the same
`Web Traffic Analysis` datasource. The Date filter is a **global (data-source-scoped) filter** stored
in the workbook's `<shared-views>` block, so it is automatically applied to *every* worksheet on that
datasource — including both graphs. The dashboard's Date range control is bound to that global filter,
so dragging it re-filters both charts at once. This is the same mechanism the original
`Web Traffic & Campaign Dashboard` used, so behaviour is consistent.

**Axis alignment fix:**
Previously only Graph 1 carried the campaign-period reference band (built from `Start Date` → `End Date`).
A reference band extends a continuous axis to include its endpoints, so Graph 1's week-axis stretched to
the campaign start/end while Graph 2's only spanned its own data — the two axes did not line up.
Graph 2 now carries the **same** campaign-period drivers:
- `Start Date` / `End Date` columns and their continuous instances were added to Graph 2.
- Two `lod` encodings (Start Date, End Date) and two paired reference lines (min Start → max End) form
  the same shaded band, with the identical `#fff2cc` fill.

With both charts using the same continuous `WEEK(Date)` axis, the same global Date filter, and the same
campaign-period band, their date axes now cover the same range and align vertically on the dashboard.

**Note on remaining pixel-level alignment:** if the left edges of the two plots still look slightly
offset on the dashboard, it is because each chart's y-axis label column can be a different width. In
Tableau Desktop this is a one-off tidy-up: select both zones and use *Distribute/!* or set a fixed
y-axis width, or simply widen the left margin of the narrower chart. It does not affect the data or the
date sync.


---

# Dashboard 2 — Total Campaign Spends

Built on the existing `Final_Campaign_Spend_Data` datasource (which already powers the
`Campaign Spending - Financial Overview` dashboard). **No existing sheets or dashboards were
changed** — everything new is prefixed with `D2 |`.

## Requirement (from `Dashboard 2 - Total Campaign Spends.png`)

| Section | Detail |
|---|---|
| Filters (single/multi) | Campaign ID, Campaign Name, Duration (start–end date), Department/School/Institute |
| Spending by Marketing Objective | Awareness, Conversion, Lead Generation |
| Spending by Marketing Channel | Digital Ads, Content Marketing, Out-of-Home (OOH) Ads, Others |
| Spends by Digital Ads | by platform (Meta, Facebook, Instagram, TikTok, LinkedIn, …) |
| Spends by Content Marketing | by platform (Mothership, The Straits Times, CNA, AsiaOne, …) |
| Spends by OOH Ads | by platform (MRT PSDC, Bus Shelter, HDB DDP, …) |
| Spends by Others | by platform (Admail, Print, …) |
| Present in chart | bar charts |

## New calculated fields (on `Final_Campaign_Spend_Data`)
`Start Date` / `End Date` are stored as **text** in the CSV, so two date calcs were added to power
the Duration filter:
- **`Campaign Start Date`** = `DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [Start Date]))`
- **`Campaign End Date`** = `DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [End Date]))`

## New worksheets (all bar charts of `SUM([Total Campaign Spend])`, currency-formatted, sorted desc)
1. **`D2 | Spend by Objective`** — spend by `Campaign Objective`.
2. **`D2 | Spend by Channel`** — spend by `Marketing Channel`.
3. **`D2 | Spend - Digital Ads`** — spend by `Marketing Platform`, pre-filtered to `Marketing Channel = Digital Ads`.
4. **`D2 | Spend - Content Marketing`** — platform spend, `Marketing Channel = Content Marketing`.
5. **`D2 | Spend - OOH Ads`** — platform spend, `Marketing Channel = Out-of-Home Ads`.
6. **`D2 | Spend - Others`** — platform spend, `Marketing Channel = Others`.

Each sheet carries open (`All`) interactive filters for Campaign ID, Campaign Name, Department, and a
Duration (Campaign Start Date) range filter.

## New dashboard — `Dashboard 2 - Total Campaign Spends`
Top to bottom: title → filter row (Campaign ID, Campaign Name, Duration, Department) → Spend by
Objective → Spend by Channel → a row of the four channel-specific platform charts (Digital Ads,
Content Marketing, OOH Ads, Others).

## Recommended manual follow-ups in Tableau Desktop
- **Scope the four shared filters to Dashboard 2's charts:** right-click each filter (Campaign ID /
  Campaign Name / Duration / Department) → *Apply to Worksheets → Selected Worksheets* and tick the six
  `D2 |` sheets. (Deliberately **not** "All Using This Data Source", so the existing
  `Campaign Spending - Financial Overview` dashboard is left untouched.)
- Verify the `Campaign Start Date` / `Campaign End Date` calcs parsed correctly (they should; the source
  format is `yyyy-MM-dd HH:mm:ss`). If your data uses a different format, adjust the `DATEPARSE` pattern.
- Optionally add data labels/percent-of-total and tidy colours per channel.

## Validation
- Workbook XML validated **well-formed** after every edit.
- All pre-existing worksheets and dashboards remain intact; only additions were made.

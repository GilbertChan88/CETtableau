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

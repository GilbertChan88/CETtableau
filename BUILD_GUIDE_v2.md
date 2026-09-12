# Web Traffic & Campaign Dashboard — Build Guide (Version 2)

**Version label:** `version-2`
**Matches workbook:** `Web Traffic Analysis.twb` at git tag `version-2`
**Tableau version:** 2024.x (workbook version 18.1)
**Locale:** English (United Kingdom) — dates display **DD/MM/YYYY**

This guide is exhaustive for the **active Version 2 deliverables** (the 4 dashboards that make up v2 and every worksheet they use). It is written so someone who has never opened the file can rebuild it from the raw CSV/Excel sources.

- **Sections 1–7** = the active v2 build (data sources → parameters → calculated fields → each worksheet → each dashboard → verification → rollback).
- **Annex A** = a full inventory of *everything* in the workbook (all 22 worksheets and all 6 dashboards), including legacy/experimental sheets that are **not** part of v2.

> **Reading the shelf notation:** `Rows: A / B` means field A then field B on the Rows shelf (nested). "Marks card" items are drop targets (Colour / Size / Label / Detail / Tooltip). Filter "mode" = how the control is shown on a dashboard (`Multiple Values (dropdown)` = multi-select checkbox list).

---

## 0. What's new in Version 2 (vs. Version 1)

| Area | Version 1 | Version 2 |
|------|-----------|-----------|
| Campaign Schedule breakdown | All platforms in one bar per campaign, coloured by **Marketing Channel** | One Gantt bar **per Marketing Platform** under each campaign |
| Field label | "Marketing Channel" | Renamed to **"Marketing Platform"** on the schedule legend + filter |
| View toggle | none | New **"Schedule View"** parameter → *Individual* (bar per platform) or *Overlap* (combined) |
| Dashboard filter | Marketing filter lived only inside the worksheet | Interactive **multi-select Marketing Platform filter** added to the Web Traffic Dashboard |

Everything else (dual-axis trend chart, date-range slider parameters, DD/MM/YYYY localisation, multi-select filters, Dashboard 1 & 2) is carried forward from v1 and fully documented below.

---

## 1. Data sources

Connect the source files (repo root) and build **three** data sources. Field names must match exactly for the calculations to work.

> **Important:** these are Tableau **Relationships** (the "noodle" model), **not** classic inner/left joins, and both relationships are keyed on **`Campaign Name for UTM`** (not "Campaign Name").

### 1.1 `Mock + Live Data`  *(used by Traffic Trend Analysis + Campaign Schedule)*
- Tables: **`Mock_WebTraffic.csv`** related to the **Campaign Master** (`Master` table from `Mock_NYP2025-001_Campaign_Master.xlsx`).
- Relationship: `Mock_WebTraffic.csv.[Campaign Name for UTM]` = `Master.[Campaign Name for UTM]`.
- Provides web-traffic measures (`Views`, `Total users`) **and** campaign attributes (`Start Date`, `End Date`, `Marketing Channel`, `Marketing Platform`).

### 1.2 `Web Traffic Analysis`  *(used by Dashboard 1 sheets + Page Performance)*
- Tables: **`Mock_WebTraffic.csv`** related to **`Mock_Campaign_Master.csv`**.
- Relationship: `[Campaign Name for UTM]` = `[Campaign Name for UTM (Mock_Campaign_Master.csv)]`.
- Adds session fields (`Sessions`, `Average session duration`, `Page path and screen class`).

### 1.3 `Final_Campaign_Spend_Data`  *(used by all Spend/Financial sheets)*
- Single table: **`Final_Campaign_Spend_Data.csv`** (one row per campaign × marketing platform, with cost columns).

### 1.4 Orphaned data sources — do not rebuild
These exist in the file but **no worksheet uses them** (leftovers from earlier iterations): `Master (standalone)`, `Mock_WebTraffic_with_live`, `Fact_Actual_Spend`, `Fact_Actual_Spend - Copy`. Safe to ignore or delete.

### 1.5 Workbook locale
Set the workbook locale to **English (United Kingdom)** so all dates render DD/MM/YYYY. (In the `.twb` this is `locale='en_GB'`.)

---

## 2. Parameters

Create these first (Data pane → **Create Parameter**).

| # | Name | Type | Allowable values | Default | Notes |
|---|------|------|------------------|---------|-------|
| P1 | **Date Granularity** | String | List: `day`, `week`, `month` (aliases **Day / Week / Month**) | `month` | drives the trend x-axis grain |
| P2 | **Date From** | Date | Range **01/01/2024 → 31/12/2025** | `01/01/2024` | format `dd/mm/yyyy` |
| P3 | **Date To** | Date | Range **01/01/2024 → 31/12/2025** | `31/03/2025` | format `dd/mm/yyyy` |
| P4 | **Schedule View** | String | List: `Individual`, `Overlap` (aliases **Individual (bar per platform)** / **Overlap (combined)**) | `Individual` | v2 toggle |

---

## 3. Calculated fields

Create in the indicated data source. (Internal calc IDs from the file are noted in brackets — you don't need to reproduce the IDs, only the names/formulas.)

### 3.1 `Mock + Live Data`
```
// Duration (Days)   [Calculation_3296071987911081986]
DATEDIFF('day', [Start Date], [End Date])

// Date (by Granularity)   [Calculation_D3GRAN01]
DATETRUNC([Parameters].[Date Granularity], [Date])

// In Range (Traffic)   [Calculation_D3RANGET01]
[Date] >= [Parameters].[Date From] AND [Date] <= [Parameters].[Date To]

// In Range (Campaign)   [Calculation_D3RANGEC01]
[Start Date] <= [Parameters].[Date To] AND [End Date] >= [Parameters].[Date From]

// Platform (View)   [Calculation_D4PLATVIEW01]   <-- THE V2 TOGGLE
IF [Parameters].[Schedule View] = "Individual" THEN [Marketing Platform] ELSE "" END

// Gantt Position (Top)   [Calculation_3296071988386656259]  (used only by legacy Traffic Trend V3)
WINDOW_MAX(SUM([Views])) * 1.1
```

### 3.2 `Web Traffic Analysis`
```
// True Avg Session Duration   [Calculation_3296071987586428928]  (weighted, not an avg-of-avgs)
SUM([Average session duration] * [Sessions]) / SUM([Sessions])

// Avg Session Duration (min sec)   [Calculation_D1DURSTR01]   -> e.g. "2min 25s"
STR(INT([True Avg Session Duration] / 60)) + "min " + STR(INT([True Avg Session Duration]) % 60) + "s"

// In Campaign Period   [Calculation_D1CAMPPERIOD01]
[Date] >= [Start Date] AND [Date] <= [End Date]
```

### 3.3 `Final_Campaign_Spend_Data`
```
// Campaign Start Date   [Calculation_D2START01]   (source stores dates as strings)
DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [Start Date]))

// Campaign End Date   [Calculation_D2END01]
DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [End Date]))

// Campaign Duration (Days)   [Calculation_D2DUR01]
DATEDIFF('day', [Campaign Start Date], [Campaign End Date])

// % of Total Spend   [Calculation_D2PCTTOTAL01]   (dynamic % of grand total)
SUM([Total Campaign Spend]) / TOTAL(SUM([Total Campaign Spend]))

// Total Spend   [Calculation_D2TOTALSPEND01]   (single friendly name for the cost columns)
[Total Campaign Spend]
```
Also on this data source: right-click **Marketing Platform → Aliases…** and rename member `Print` → **`Brochures`**.

---

## 4. Worksheets (active v2)

For each: data source, mark type, shelves, marks-card encodings, filters (+ default state), sorts, formatting.

### 4.1 Campaign Schedule ⭐ (core v2 change) — DS: `Mock + Live Data`
- **Mark type:** Gantt Bar.
- **Columns:** `Start Date` (exact date, continuous).
- **Rows:** `Campaign Name` **/** `Platform (View)`  → each campaign gets one sub-row per platform when *Individual*.
- **Marks card:** Colour = **Marketing Platform**; Size = `AVG(Duration (Days))` (bar length); mark transparency ≈ 77%.
- **Filters:**
  1. **Marketing Platform** — *Show all members*; on the dashboard show as **Multiple Values (dropdown)** (multi-select).
  2. **In Range (Campaign)** = `True` — ties the schedule to the date slider (keeps only campaigns overlapping P2–P3).
- **Sort:** Campaign Name **ascending** by `AVG(Duration (Days))`.
- **Behaviour of the toggle:** *Schedule View = Individual* → `Platform (View)` = the platform → one row per platform. *Overlap* → `Platform (View)` = `""` → all platforms collapse to a single row per campaign (bars overlap, still colour-coded).

### 4.2 Traffic Trend Analysis — DS: `Mock + Live Data`
- **Mark type:** dual-axis combo — **Bar** (`SUM(Views)`) + **Line** (`SUM(Total users)`), axes synchronised, one colour legend via **Measure Names**.
- **Columns:** **Date (by Granularity)** (continuous) — respects the P1 Day/Week/Month parameter; supports >12 buckets in chronological order.
- **Rows:** `SUM(Views)` + `SUM(Total users)` (Measure Values as dual axis).
- **Marks card:** Colour = **Measure Names**; Label = `SUM(Views)` on the bar; Tooltip = `SUM(Views)`, `SUM(Total users)`.
- **Filters:**
  1. **In Range (Traffic)** = `True` (date-slider sync).
  2. **Campaign ID** — show all (multi-select on dashboard).
  3. **Dept/Sch/Institute** — multi-select (the file ships with a saved selection of `C&O`; clear/adjust as needed).
- **Header date format:** `MMM-YY`.

### 4.3 Page Performance Details — DS: `Web Traffic Analysis`
- **Mark type:** Automatic (text table).
- **Columns:** `Measure Names`.
- **Rows:** `Campaign ID` / (`Campaign Name` / `Page path and screen class`).
- **Marks card:** Text = `Measure Values` (Multiple Values). Include **`Views`**, **`Total users`**, and **`Avg Session Duration (min sec)`** (the weighted "xx min xx s" string) among the Measure Values.
- **Filters:**
  1. **Measure Names** (choose which metric columns show).
  2. **Campaign ID** — show all.
  3. **Campaign Name** — exclude `Null`.
  4. **Page path and screen class** — show all, **Multiple Values (dropdown)** so users can find parent pages.
- **Sort:** Page path descending.

### 4.4 D1 | Traffic - All CET Pages — DS: `Web Traffic Analysis`
- **Mark type:** dual-axis combo — **Bar** (`SUM(Views)`) + **Line** (`SUM(Total users)`), synchronised.
- **Columns:** `WEEK(Date)` (continuous truncated date).
- **Rows:** `SUM(Views)` + `SUM(Total users)`.
- **Marks card:** Colour = **Measure Names**; Detail = `Start Date`, `End Date` (for campaign-period reference); Label = `SUM(Views)`; Tooltip = `SUM(Views)`, `SUM(Total users)`.
- **Filters (all multi-select / show-all):** Campaign ID, Campaign Name, Dept/Sch/Institute, Page path and screen class.

### 4.5 D1 | Traffic - Selected Pages — DS: `Web Traffic Analysis`
- **Mark type:** Line.
- **Columns:** `WEEK(Date)`.
- **Rows:** `SUM(Views)`.
- **Marks card:** Colour = **Page path and screen class**; Detail = `Start Date`, `End Date`; Tooltip = `SUM(Views)`, `SUM(Total users)`.
- **Filters:** Campaign ID, Campaign Name, Dept/Sch/Institute, Page path and screen class (the Page-path filter is the "selected pages" control).

### 4.6 D1 | Key Metrics — DS: `Web Traffic Analysis`
- **Mark type:** Automatic (KPI text tiles).
- **Columns:** `Measure Names`.
- **Rows:** `Page path and screen class`.
- **Marks card:** Text = `Measure Values` (Multiple Values).
- **Filters:** Measure Names (which KPIs), Campaign ID, Campaign Name, Dept/Sch/Institute (all show-all).
- **Sort:** Page path descending.

### 4.7 Spend by Dept — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Bar.
- **Columns:** `Dept/Sch/Institute`.
- **Rows:** `SUM(Total Campaign Spend)`.
- **Marks card:** Colour = **Campaign Type**; Tooltip = `SUM(Total Campaign Spend)`.
- **Sort:** Dept/Sch/Institute **descending** by spend.
- **Format:** spend axis/labels as currency `$#,##0`.

### 4.8 Channel Mix — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Automatic → **Treemap** (Size + Colour both `SUM(Total Campaign Spend)`).
- **Detail (LOD):** `Marketing Platform`.
- **Marks card / Label:** `Marketing Channel`, `Marketing Platform`, `SUM(Total Campaign Spend)`, and **`% of Total Spend`** (dynamic).
- Make this the **main/left focus** of the financial dashboard.

### 4.9 Cost Details — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Automatic (text table).
- **Columns:** `Measure Names`.
- **Rows:** `Campaign Name` / (`Marketing Channel` / `Marketing Platform`).
- **Marks card:** Text = `Measure Values` (Multiple Values).
- **Filters:** **Measure Names** (choose columns), **Campaign Name** (multi-select). Include **Campaign Start Date** / **Campaign End Date** columns right after the name, and a **Total Spend** column (rename the three cost components to a single "Total Spend").

### 4.10 KPI Banner — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Text.
- **Marks card:** Text = `SUM(Total Campaign Spend)` (single big-number tile). Format as currency.

### 4.11 D2 | Spend by Objective — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Bar. **Columns:** `SUM(Total Campaign Spend)`. **Rows:** `Campaign Objective`.
- **Marks card:** Colour = **Campaign Objective**; Label = `SUM(Total Campaign Spend)`.
- **Sort:** Campaign Objective descending by spend.
- **Filters (shared, multi-select):** Campaign ID, Campaign Name, Dept/Sch/Institute; plus **Campaign Start Date** (date range) — these are the dashboard's standard filter set.

### 4.12 D2 | Spend by Channel — DS: `Final_Campaign_Spend_Data`
- **Mark type:** Bar. **Columns:** `SUM(Total Campaign Spend)`. **Rows:** `Marketing Channel`.
- **Marks card:** Colour = **Marketing Channel**; Label = `SUM(Total Campaign Spend)`.
- **Sort:** Marketing Channel descending by spend.
- **Filters:** same shared set as 4.11.

### 4.13 D2 | Spend – Digital Ads / Content Marketing / OOH Ads / Others  (4 sheets, identical template) — DS: `Final_Campaign_Spend_Data`
Build one, then duplicate three times and change only the locked channel filter:
- **Mark type:** Bar. **Columns:** `SUM(Total Campaign Spend)`. **Rows:** `Marketing Platform`.
- **Marks card:** Colour = **Marketing Platform**; Label = `SUM(Total Campaign Spend)`.
- **Sort:** Marketing Platform descending by spend.
- **Locked filter (the only difference):** `Marketing Channel` = one of `Digital Ads` / `Content Marketing` / `Out-of-Home Ads` / `Others`.
- **Filters (shared):** Campaign ID, Campaign Name, Dept/Sch/Institute, Campaign Start Date.

---

## 5. Dashboards (active v2)

Each dashboard uses a top **filter/parameter strip** (a horizontal layout container) above the charts. Filter cards are shown as **Multiple Values (dropdown)** unless noted.

### 5.1 Web Traffic Dashboard  ⭐ (primary v2 surface)
**Sheets:** Traffic Trend Analysis, Campaign Schedule, Page Performance Details.
**Filter strip (left → right):**
1. **Date From** — parameter control (P2), **slider**.
2. **Date To** — parameter control (P3), **slider**.
3. **Date Granularity** — parameter control (P1), **compact** dropdown.
4. **Schedule View** — parameter control (P4), **compact** dropdown. ⭐ *new in v2*
5. **Campaign Name for UTM** — filter (Traffic Trend Analysis), multi-select.
6. **Dept/Sch/Institute** — filter (Traffic Trend Analysis), multi-select.
7. **Campaign ID** — filter (Traffic Trend Analysis), multi-select.
8. **Marketing Platform** — filter (**Campaign Schedule**), multi-select. ⭐ *new in v2*
9. Colour legends: **Measure Names** (Traffic Trend Analysis) and **Marketing Platform** (Campaign Schedule).

**Body:** Traffic Trend Analysis chart, then Campaign Schedule chart. A hidden **Date** filter on Traffic Trend Analysis is also present.
> To add the Marketing Platform filter: select the Campaign Schedule zone → **More options → Filters → Marketing Platform**, set the card to **Multiple Values (dropdown)**, and drag it into the strip.

### 5.2 Dashboard 1 - Total Web Traffic
**Sheets:** D1 | Key Metrics, D1 | Traffic - All CET Pages, D1 | Traffic - Selected Pages.
**Filters (on D1 | Traffic - All CET Pages, shown top strip):** Campaign ID, Campaign Name, Dept/Sch/Institute (multi-select), **Date** (range), **Page path and screen class** (multi-select). Plus a **Page path** filter on D1 | Traffic - Selected Pages (drives the selected-pages line chart).
**Body:** Key Metrics tiles on top; "All CET Pages" dual-axis combo (Graph 1) and "Selected Pages" line chart below. Dates DD/MM/YYYY.

### 5.3 Dashboard 2 - Total Campaign Spends
**Sheets:** D2 | Spend by Objective, D2 | Spend by Channel, D2 | Spend – Digital Ads, – Content Marketing, – OOH Ads, – Others.
**Filters (standardised top-right):** Campaign ID, Campaign Name, Dept/Sch/Institute (multi-select), **Campaign Start Date** (range). Add a **Campaign Objective** filter if desired (Awareness/Conversion/Lead Gen).
**Body:** Spend by Objective and Spend by Channel as the summaries; the four channel-specific platform breakdowns beneath.

### 5.4 Campaign Spending - Financial Overview
**Sheets:** KPI Banner, Channel Mix, Spend by Dept, Cost Details.
**Controls:** filter **Campaign Name** (Cost Details); filters **Campaign Objective** + **Campaign Type** (Spend by Dept), multi-select; colour legends — **Campaign Type** (Spend by Dept) and **Total Campaign Spend** (Channel Mix).
**Layout intent:** KPI Banner across the top; **Channel Mix on the left as the main focus**; **Spend by Dept on the right**; Cost Details table beneath. Different colour palettes for Channel Mix vs. Spend by Dept.

---

## 6. Acceptance checklist (v2)

- [ ] Campaign Schedule shows **one bar per Marketing Platform** under each campaign when *Schedule View = Individual*.
- [ ] *Schedule View = Overlap* collapses each campaign to a single combined row.
- [ ] The **Marketing Platform** dropdown on the Web Traffic Dashboard multi-selects and filters the schedule.
- [ ] Schedule legend + filter read **Marketing Platform** (not "Marketing Channel").
- [ ] Date controls are **sliders**, display **DD/MM/YYYY**, and both trend + schedule respect the range.
- [ ] Trend x-axis switches Day/Week/Month via the granularity parameter and stays chronological beyond 12 buckets, labelled **MMM-YY**.
- [ ] Page Performance shows session duration as **"x min y s"** (weighted), with a Page-path filter.
- [ ] Spend views show `Print` as **Brochures**; Channel Mix shows **% of total**; Cost Details shows start/end dates + a single **Total Spend**.

---

## 7. Rollback

- **Version 2 tag:** `version-2` (workbook + this guide).
- **Earlier verified build:** tag `verified-working-2026-08-18`.
```
git checkout version-2 -- "Web Traffic Analysis.twb"
```

---
---

# Annex A — Full inventory (all 22 worksheets + 6 dashboards)

This annex documents **everything** in the file, including legacy/experimental items that are **not** part of v2. Use it for auditing or clean-up. "Status" marks whether an item is part of the active v2 build.

## A.1 All worksheets (22)

| # | Worksheet | Data source | Mark | Rows | Columns | Colour / Size | Key filters | Status |
|---|-----------|-------------|------|------|---------|---------------|-------------|--------|
| 1 | **Campaign Schedule** | Mock + Live Data | GanttBar | Campaign Name / Platform (View) | Start Date | Colour Marketing Platform; Size AVG(Duration Days) | Marketing Platform (all); In Range (Campaign)=true | ✅ active (§4.1) |
| 2 | Campaign Schedule 2 | — (none) | Automatic | (empty) | (empty) | — | — | 🗑 empty stub — delete |
| 3 | **Channel Mix** | Final_Campaign_Spend | Automatic→Treemap | (detail) | — | Size+Colour SUM(Total Campaign Spend); Detail Marketing Platform | (dashboard action) | ✅ active (§4.8) |
| 4 | **Cost Details** | Final_Campaign_Spend | Text table | Campaign Name / (Marketing Channel / Marketing Platform) | Measure Names | Text=Measure Values | Measure Names; Campaign Name | ✅ active (§4.9) |
| 5 | **KPI Banner** | Final_Campaign_Spend | Text | (empty) | (empty) | Text SUM(Total Campaign Spend) | — | ✅ active (§4.10) |
| 6 | **Page Performance Details** | Web Traffic Analysis | Text table | Campaign ID / (Campaign Name / Page path) | Measure Names | Text=Measure Values | Measure Names; Campaign ID; Campaign Name(excl null); Page path | ✅ active (§4.3) |
| 7 | **Spend by Dept** | Final_Campaign_Spend | Bar | SUM(Total Campaign Spend) | Dept/Sch/Institute | Colour Campaign Type | — (sort desc) | ✅ active (§4.7) |
| 8 | Traffic Trend | Web Traffic Analysis | Bar+Line combo | SUM(Views)+SUM(Total users) | WEEK(Date) | Colour Measure Names | Campaign ID/Name/Dept/Page path (union) | ⚠ legacy (v1 combo, weekly only) |
| 9 | **Traffic Trend Analysis** | Mock + Live Data | Bar+Line combo | SUM(Views)+SUM(Total users) | Date (by Granularity) | Colour Measure Names | In Range (Traffic)=true; Campaign ID; Dept/Sch/Institute(=C&O) | ✅ active (§4.2) |
| 10 | Traffic Trend Analysis (v2) | Mock + Live Data | Bar+Line combo | SUM(Views)+SUM(Total users) | WEEK(Date) | Colour Measure Names; Detail Start/End Date | Campaign ID; Dept/Sch/Institute(=C&O) | ⚠ legacy (not on any dashboard) |
| 11 | Traffic Trend Analysis (v4) | Mock + Live Data | Bar+Line combo | SUM(Views)+SUM(Total users) | WEEK(Date) | Colour Measure Names; Tooltip Page path | Campaign ID; Campaign Name(=CET B2C…Q1 2025); Dept(=C&O); Page path | ⚠ legacy (on v0.2 dashboard) |
| 12 | Traffic Trend V3 | Mock + Live Data | Bar + GanttBar | SUM(Views)+usr:Gantt Position | WEEK(Date) | Bar colour Measure Names; Gantt colour Marketing Channel, size SUM(Duration Days), detail Campaign Name | — | ⚠ legacy experiment (traffic+gantt overlay) |
| 13 | **D1 \| Traffic - All CET Pages** | Web Traffic Analysis | Bar+Line combo | SUM(Views)+SUM(Total users) | WEEK(Date) | Colour Measure Names; Detail Start/End Date | Campaign ID/Name/Dept/Page path (all) | ✅ active (§4.4) |
| 14 | **D1 \| Traffic - Selected Pages** | Web Traffic Analysis | Line | SUM(Views) | WEEK(Date) | Colour Page path | Campaign ID/Name/Dept/Page path (all) | ✅ active (§4.5) |
| 15 | **D1 \| Key Metrics** | Web Traffic Analysis | Text tiles | Page path | Measure Names | Text=Measure Values | Measure Names; Campaign ID/Name/Dept | ✅ active (§4.6) |
| 16 | **D2 \| Spend by Objective** | Final_Campaign_Spend | Bar | Campaign Objective | SUM(Total Campaign Spend) | Colour Campaign Objective; Label spend | Campaign ID/Name/Dept; Campaign Start Date | ✅ active (§4.11) |
| 17 | **D2 \| Spend by Channel** | Final_Campaign_Spend | Bar | Marketing Channel | SUM(Total Campaign Spend) | Colour Marketing Channel; Label spend | Campaign ID/Name/Dept; Campaign Start Date | ✅ active (§4.12) |
| 18 | **D2 \| Spend - Digital Ads** | Final_Campaign_Spend | Bar | Marketing Platform | SUM(Total Campaign Spend) | Colour Marketing Platform; Label spend | Marketing Channel=Digital Ads (+ shared) | ✅ active (§4.13) |
| 19 | **D2 \| Spend - Content Marketing** | Final_Campaign_Spend | Bar | Marketing Platform | SUM(Total Campaign Spend) | Colour Marketing Platform; Label spend | Marketing Channel=Content Marketing (+ shared) | ✅ active (§4.13) |
| 20 | **D2 \| Spend - OOH Ads** | Final_Campaign_Spend | Bar | Marketing Platform | SUM(Total Campaign Spend) | Colour Marketing Platform; Label spend | Marketing Channel=Out-of-Home Ads (+ shared) | ✅ active (§4.13) |
| 21 | **D2 \| Spend - Others** | Final_Campaign_Spend | Bar | Marketing Platform | SUM(Total Campaign Spend) | Colour Marketing Platform; Label spend | Marketing Channel=Others (+ shared) | ✅ active (§4.13) |
| 22 | Campaign Schedule by Platform | Final_Campaign_Spend | GanttBar | Campaign Name / Marketing Platform | Campaign Start Date | Colour Marketing Platform; Size SUM(Campaign Duration Days) | Campaign ID/Name/Dept; Campaign Start Date | ⚠ legacy alternative — see note below |

**Note on #22 (Campaign Schedule by Platform):** this is an *alternative* per-platform schedule built on `Final_Campaign_Spend_Data`. It was **not** adopted for v2 because that data source is **not** wired to the Web Traffic Dashboard's date-slider parameters (P2/P3), so it would not stay in sync with the trend chart. v2 instead put the per-platform logic on the **Campaign Schedule** sheet (Mock + Live Data), which does honour the date slider via `In Range (Campaign)`.

### Legacy calc used only by Annex sheets
`Gantt Position (Top) = WINDOW_MAX(SUM([Views])) * 1.1` (Mock + Live Data) — used only by **Traffic Trend V3** (#12) to place the Gantt overlay above the bars.

## A.2 All dashboards (6)

| # | Dashboard | Sheets | Controls | Status |
|---|-----------|--------|----------|--------|
| 1 | **Campaign Spending - Financial Overview** | KPI Banner, Channel Mix, Spend by Dept, Cost Details | Filters: Cost Details→Campaign Name; Spend by Dept→Campaign Objective + Campaign Type. Colour legends: Campaign Type, Total Campaign Spend | ✅ active (§5.4) |
| 2 | Web Traffic & Campaign Dashboard | Traffic Trend, Page Performance Details | Filters (Traffic Trend): Date, Campaign ID, Dept/Sch/Institute, Campaign Name; Colour Measure Names | ⚠ legacy (v1) |
| 3 | Web Traffic & Campaign Dashboard (v0.2) | Campaign Schedule, Traffic Trend Analysis (v4), Page Performance Details | Filters: Page Performance→Page path, Date; TTA(v4)→Campaign Name/Dept/Campaign ID; Colour Measure Names | ⚠ legacy (v0.2) |
| 4 | **Web Traffic Dashboard** | Traffic Trend Analysis, Campaign Schedule, Page Performance Details | Params P1/P2/P3/P4; filters TTA→Campaign Name for UTM/Dept/Campaign ID + Date; Campaign Schedule→Marketing Platform; colours Measure Names + Marketing Platform | ✅ active — **primary v2** (§5.1) |
| 5 | **Dashboard 1 - Total Web Traffic** | D1 \| Key Metrics, D1 \| Traffic - All CET Pages, D1 \| Traffic - Selected Pages | Filters: Campaign ID/Name/Dept, Date, Page path (All CET Pages); Page path (Selected Pages) | ✅ active (§5.2) |
| 6 | **Dashboard 2 - Total Campaign Spends** | D2 \| Spend by Objective / by Channel / - Digital Ads / - Content Marketing / - OOH Ads / - Others | Filters: Campaign ID/Name/Dept, Campaign Start Date | ✅ active (§5.3) |

## A.3 Suggested clean-up (optional)
Not required for v2, but if you want a lean workbook, these can be deleted safely (nothing active depends on them):
- Worksheets: Campaign Schedule 2, Traffic Trend, Traffic Trend Analysis (v2), Traffic Trend Analysis (v4), Traffic Trend V3, Campaign Schedule by Platform.
- Dashboards: Web Traffic & Campaign Dashboard, Web Traffic & Campaign Dashboard (v0.2).
- Data sources: Master (standalone), Mock_WebTraffic_with_live, Fact_Actual_Spend, Fact_Actual_Spend - Copy.

> ⚠ Deleting Traffic Trend Analysis (v4) will also require removing dashboard (v0.2). Do clean-up on a separate branch and re-validate the file opens before merging.

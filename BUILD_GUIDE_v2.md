# Web Traffic & Campaign Dashboard — Build Guide (Version 2)

**Version label:** `version-2`
**Matches workbook:** `Web Traffic Analysis.twb` at git tag `version-2` (commit `5c2e482`)
**Tableau version:** 2024.x (workbook version 18.1)
**Locale:** English (United Kingdom) — dates display as **DD/MM/YYYY**

---

## 0. What's new in Version 2 (vs. Version 1)

| Area | Version 1 | Version 2 |
|------|-----------|-----------|
| Campaign Schedule breakdown | All platforms in one bar per campaign, coloured by **Marketing Channel** | One bar **per Marketing Platform** under each campaign |
| Field label | "Marketing Channel" | Renamed to **"Marketing Platform"** on the schedule legend/filter |
| View toggle | none | New **"Schedule View"** parameter → *Individual* (bar per platform) or *Overlap* (combined) |
| Dashboard filter | Marketing filter only inside the worksheet | Interactive **multi-select Marketing Platform filter** on the Web Traffic Dashboard |

Everything else (dual-axis Graph 1, date-range slider parameters, DD/MM/YYYY localisation, multi-select filters, Dashboard 1 & 2) is carried forward from Version 1 and documented below so the build is reproducible from scratch.

---

## 1. Prerequisites — data sources

Connect these files (all in the repo root) and build the following **data sources**. Field names must match exactly for the calculations below to work.

| Data source (caption) | Built from | Join | Used by |
|-----------------------|-----------|------|---------|
| **Web Traffic Analysis** | `Mock_WebTraffic.csv` + `Mock_Campaign_Master.csv` | Left join on `Campaign Name for UTM` | Dashboard 1 sheets, Page Performance |
| **Mock + Live Data** | `Mock_WebTraffic.csv` + Campaign Master (`Master`) | Left join on Campaign Name | Traffic Trend Analysis, **Campaign Schedule** |
| **Final_Campaign_Spend_Data** | `Final_Campaign_Spend_Data.csv` | single table | all Spend sheets |

> The Campaign Master (`Mock_NYP2025-001_Campaign_Master.xlsx` / CSV export) is where **Marketing Channel** (broad category: Digital Ads, Content Marketing, Out-of-Home Ads, Others) and **Marketing Platform** (specific: Facebook, TikTok, Google Search, Bus Shelter Posters, etc.) live. Each campaign can have **multiple platform rows** — that is what enables the per‑platform bars.

---

## 2. Parameters (create these first)

Right‑click in the Data pane → **Create Parameter**.

| # | Name | Data type | Allowable values | Default | Notes |
|---|------|-----------|------------------|---------|-------|
| P1 | **Date Granularity** | String | List: `day`, `week`, `month` | `month` | Display aliases: Day / Week / Month |
| P2 | **Date From** | Date | Range (min = earliest date, max = latest) | `01/01/2024` | Format `dd/mm/yyyy` |
| P3 | **Date To** | Date | Range | `31/03/2025` | Format `dd/mm/yyyy` |
| P4 | **Schedule View** | String | List: `Individual`, `Overlap` | `Individual` | Aliases: `Individual (bar per platform)`, `Overlap (combined)` |

---

## 3. Calculated fields

Create these in the indicated data source (Data pane → **Create Calculated Field**).

### 3a. Mock + Live Data
```
// Duration (Days)
DATEDIFF('day', [Start Date], [End Date])

// Date (by Granularity)
DATETRUNC([Parameters].[Date Granularity], [Date])

// In Range (Traffic)   -- keeps only traffic within the date slider
[Date] >= [Parameters].[Date From] AND [Date] <= [Parameters].[Date To]

// In Range (Campaign)  -- keeps campaigns overlapping the date slider
[Start Date] <= [Parameters].[Date To] AND [End Date] >= [Parameters].[Date From]

// Platform (View)  -- THE V2 TOGGLE
IF [Parameters].[Schedule View] = "Individual"
THEN [Marketing Platform]
ELSE ""
END
```

### 3b. Web Traffic Analysis
```
// True Avg Session Duration  -- weighted, not a sum of averages
SUM([Average session duration] * [Sessions]) / SUM([Sessions])

// Avg Session Duration (min sec)  -- e.g. "2min 25s"
STR(INT([True Avg Session Duration] / 60)) + "min "
+ STR(INT([True Avg Session Duration]) % 60) + "s"

// In Campaign Period
[Date] >= [Start Date] AND [Date] <= [End Date]
```

### 3c. Final_Campaign_Spend_Data
```
// Campaign Start Date  (source stores it as a string)
DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [Start Date]))

// Campaign End Date
DATE(DATEPARSE("yyyy-MM-dd HH:mm:ss", [End Date]))

// Campaign Duration (Days)
DATEDIFF('day', [Campaign Start Date], [Campaign End Date])

// % of Total Spend  (dynamic % of grand total)
SUM([Total Campaign Spend]) / TOTAL(SUM([Total Campaign Spend]))

// Total Spend  (single rename for the three cost components)
[Total Campaign Spend]
```

Also on this data source: right‑click **Marketing Platform** → **Aliases…** and rename the member `Print` → **`Brochures`**.

---

## 4. Worksheets

### 4.1 Campaign Schedule ⭐ (the main V2 change)
Data source: **Mock + Live Data**. Mark type: **Gantt Bar**.

1. **Rows:** drag **Campaign Name**, then drag **Platform (View)** to the right of it → shelf reads `Campaign Name / Platform (View)`.
2. **Columns:** **Start Date** (exact date, continuous).
3. **Marks → Size:** `AVG(Duration (Days))` (length of each gantt bar).
4. **Marks → Colour:** **Marketing Platform** (each platform gets its own colour).
5. **Filters:**
   - **Marketing Platform** → show all members; on the card choose **Multiple Values (dropdown)** so it is a checkbox multi-select.
   - **In Range (Campaign)** → keep **True** (ties the schedule to the date slider).
6. Sort Campaign Name ascending by `AVG(Duration (Days))`.
7. Set mark transparency ~77%.

**Behaviour:**
- *Schedule View = Individual* → `Platform (View)` returns the platform, so each campaign shows one row per platform.
- *Schedule View = Overlap* → `Platform (View)` returns `""`, collapsing all platforms into a single row per campaign (bars overlap, still colour‑coded).

### 4.2 Traffic Trend Analysis
Data source: **Mock + Live Data**. Bar + line combo.
- Columns: **Date (by Granularity)** (responds to the granularity parameter — day/week/month; more than 12 bars supported, chronologically ordered).
- Rows: `SUM(Views)` (bars) and a second measure for the line (dual axis, synchronised).
- Filter: **In Range (Traffic)** = True.
- Header date format: `MMM-YY`.

### 4.3 Dashboard 1 sheets (Data source: Web Traffic Analysis)
- **D1 | Traffic - All CET Pages** — bar+line dual axis of Views/Users over `Date (by Granularity)`, with a **Page path and screen class** filter (multi-select).
- **D1 | Traffic - Selected Pages** — same measures filtered to selected pages.
- **D1 | Key Metrics** — KPI tiles.
- **Page Performance Details** — table showing **Avg Session Duration (min sec)** (the weighted "xx min xx s" version) plus a **Page path and screen class** filter.

### 4.4 Dashboard 2 / Spend sheets (Data source: Final_Campaign_Spend_Data)
- **Channel Mix** — bar of `SUM(Total Campaign Spend)` by Marketing Platform with **% of Total Spend** label (dynamic).
- **Spend by Dept** — spend by `Dept/Sch/Institute`.
- **Cost Details** — table by Campaign Name with **Campaign Start Date / Campaign End Date** right after the name and a **Total Spend** column.
- **D2 | Spend by Objective / Channel / Digital Ads / Content Marketing / OOH Ads / Others** — breakdown sheets.

---

## 5. Dashboards

### 5.1 Web Traffic Dashboard (primary — carries the V2 controls)
Layout, top to bottom:
1. **Title** row.
2. **Filter strip** (a horizontal *layout container*) containing, left→right:
   - **Date From** (slider), **Date To** (slider) — parameter controls.
   - **Date Granularity** (compact dropdown) — parameter control.
   - **Schedule View** (compact dropdown) — parameter control ⭐ *new in V2*.
   - **Campaign Name for UTM**, **Dept/Sch/Institute**, **Campaign ID** filters (multi-select dropdowns, apply to Traffic Trend Analysis).
   - **Marketing Platform** filter (multi-select dropdown) ⭐ *new in V2* — added from the **Campaign Schedule** sheet so it filters the schedule directly on the dashboard.
   - **Measure Names** and **Marketing Platform** colour legends.
3. **Traffic Trend Analysis** chart.
4. **Campaign Schedule** chart.

> To add the Marketing Platform filter to the dashboard: select the Campaign Schedule zone → **More options → Filters → Marketing Platform**, then set the card to **Multiple Values (dropdown)** and drag it into the filter strip.

### 5.2 Dashboard 1 - Total Web Traffic
Graph 1 as a **dual-axis** chart (synchronised axes), a **Page** selector filter, and the shared date slider driving the view. Dates localised to DD/MM/YYYY.

### 5.3 Dashboard 2 - Total Campaign Spends
Channel Mix (left, main focus) + Spend by Dept (right) + Cost Details, with Campaign Type / Campaign Name / Campaign Objective / Campaign ID / Date filters standardised to the top‑right.

### 5.4 Campaign Spending - Financial Overview
Financial roll‑up dashboard (Channel Mix, Spend by Dept, Cost Details) using Final_Campaign_Spend_Data.

---

## 6. Verify (acceptance checklist for V2)

- [ ] Campaign Schedule shows **one bar per Marketing Platform** under each campaign when *Schedule View = Individual*.
- [ ] Switching *Schedule View = Overlap* collapses each campaign back to a single combined row.
- [ ] The **Marketing Platform** dropdown on the Web Traffic Dashboard filters the schedule (multi-select).
- [ ] Legend and filter both read **Marketing Platform** (not "Marketing Channel").
- [ ] Date controls are sliders and display **DD/MM/YYYY**; charts respect the range.
- [ ] `Print` shows as **Brochures** in the spend views.

---

## 7. Rollback

If a change breaks the workbook, restore the last known-good build:
- **Version 2 tag:** `version-2` (commit `5c2e482`)
- **Earlier verified build:** tag `verified-working-2026-08-18` (commit `5b61ffb`)

```
git checkout version-2 -- "Web Traffic Analysis.twb"
```

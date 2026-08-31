# Power BI Build Guide — Web Traffic & Campaign (replica of Tableau version-2)

This guide recreates the **version-2** Tableau dashboards (`Web Traffic Analysis.twb`, tag `version-2` on branch `dashboard1-web-traffic-improvements`) in **Power BI Desktop**.

It maps each Tableau data source, calculation, parameter and dashboard to its Power BI equivalent. Everything here is copy-paste reliable — the Power Query (`powerquery/`) and DAX (`dax/`) files are ready to use.

> **Why a guide + PBIP source instead of a `.pbix`?** A `.pbix` is a binary that can't be authored/validated outside Power BI Desktop. This repo ships the **PBIP** source format (TMDL semantic model + PBIR report) plus this build kit. Open the PBIP in Power BI Desktop (Dec 2023+ with *File ▸ Options ▸ Preview features ▸ Power BI Project (.pbip) save option* enabled), **or** build from scratch with the steps below — both produce the same result.

---

## 0. Source data → Power BI tables

| Source file | Power BI table | Role |
|-------------|----------------|------|
| `Mock_WebTraffic.csv` | **WebTraffic** | fact: Views, Total users, Sessions, Avg session duration by Date × Page × UTM |
| `Final_Campaign_Spend_Data.csv` | **CampaignSpend** | fact + attributes: one row per campaign × marketing platform, with costs + Start/End dates |
| *(derived from CampaignSpend)* | **Campaign** | dimension: one row per `Campaign Name for UTM` (relates web traffic to campaign attributes) |
| *(generated)* | **Calendar** | date dimension for the trend axis + Day/Week/Month switching |
| `Fact_Actual_Spend.csv` | **FactActualSpend** | optional (not used by the core version-2 pages) |

### 0.1 Load the data
1. **File ▸ Options ▸ Preview features** → tick **Power BI Project (.pbip) save option** (so you can save as source).
2. **Home ▸ Transform data** to open Power Query.
3. **Manage Parameters ▸ New** → create a Text parameter **`SourceFolder`** = the folder containing the CSVs, with a trailing backslash (e.g. `C:\Users\you\CETtableau\`). See `powerquery/00_Parameters.m`.
4. For each table, **New Source ▸ Blank Query ▸ Advanced Editor**, then paste the matching script from `powerquery/`:
   - `WebTraffic.m`, `CampaignSpend.m`, `Campaign.m`, `Calendar.m`, `FactActualSpend.m`
5. **Close & Apply**.

### 0.2 Relationships (Model view)
Create these (drag the field from the first table onto the second):
- **Campaign[Campaign Name for UTM] → WebTraffic[Campaign Name for UTM]** — 1-to-many, single direction.
- **Calendar[Date] → WebTraffic[Date]** — 1-to-many, single direction. Mark **Calendar** as a date table (Table tools ▸ Mark as date table ▸ `Date`).
- **CampaignSpend** stays standalone (it carries its own Dept / Channel / Platform / Objective attributes, exactly like the Tableau *Final_Campaign_Spend_Data* source).

### 0.3 Measures & calculated columns
- Add every measure from `dax/measures.dax` (New measure).
- Add the calculated columns from `dax/calculated_columns.dax` (New column).

**Calc mapping (Tableau → Power BI):**

| Tableau calc | Power BI |
|--------------|----------|
| True Avg Session Duration | `Weighted Avg Session Duration (s)` measure |
| Avg Session Duration (min sec) | `Avg Session Duration (min sec)` measure |
| % of Total Spend | `% of Total Spend` measure (`DIVIDE` + `ALLSELECTED`) |
| Total Spend / Total Media/Production/Agency | corresponding `Total …` measures |
| Duration (Days) / Campaign Duration (Days) | `Campaign Duration (Days)` calc column |
| Date (by Granularity) [Param 1] | **Date Granularity** field parameter (§1) |
| In Range (Traffic) / In Range (Campaign) [Params 2/3] | the **Date slicer** on `Calendar[Date]` (relationships handle it) |
| Platform (View) [Param 4] | **Schedule View** field parameter (§1) |
| Marketing Platform alias Print→Brochures | handled in `CampaignSpend.m` |

---

## 1. Parameters (Tableau parameters → Power BI)

Power BI doesn't use Tableau-style parameters; use these idiomatic equivalents:

- **Date From / Date To** (Tableau P2/P3) → a **Slicer** visual on `Calendar[Date]`, slicer style **Between**. It filters every visual related to Calendar (the trend chart + table). This replaces the "In Range" boolean calcs.
- **Date Granularity** (Tableau P1) → a **Field Parameter**: *Modeling ▸ New parameter ▸ Fields*, name **`Date Granularity`**, add (in order) `Calendar[Date]` (rename "Day"), `Calendar[Week Start]` ("Week"), `Calendar[Month-Year]` ("Month"). Tick "Add slicer". Set `Month-Year` Sort-by to `Month Sort`.
- **Schedule View** (Tableau P4, Individual/Overlap) → a **Field Parameter** named **`Schedule View`** with `CampaignSpend[Marketing Platform]` ("Individual (bar per platform)") and `CampaignSpend[Campaign Name]` ("Overlap (combined)"). Used on the Campaign Schedule visual's group field. (Details in `dax/calculated_columns.dax`.)

---

## 2. Page: **Web Traffic Dashboard** (primary)

Recreates the Tableau *Web Traffic Dashboard* (Traffic Trend Analysis + the summary table + Campaign Schedule).

**Top slicer strip (left→right):**
1. **Slicer** – `Calendar[Date]`, style **Between** (= Date From/Date To).
2. **Slicer** – **Date Granularity** field parameter (dropdown).
3. **Slicer** – **Schedule View** field parameter (dropdown).
4. **Slicer** – `Campaign[Campaign Name]` (dropdown, multi-select).
5. **Slicer** – `Campaign[Dept/Sch/Institute]` (dropdown, multi-select).
6. **Slicer** – `Campaign[Campaign ID]` (dropdown, multi-select).
7. **Slicer** – `CampaignSpend[Marketing Platform]` (dropdown, multi-select) — for the schedule.

**Visual A — Traffic Trend (line + column combo)** *(= "Traffic Trend Analysis")*
- Visual type: **Line and clustered column chart**.
- X-axis: the **Date Granularity** field parameter.
- Column y-axis: `[Total Views]`.
- Line y-axis: `[Total Users]`.
- This gives the dual-axis trend that switches Day/Week/Month via the granularity slicer, chronological, unlimited buckets, labelled `MMM yy`.

**Visual B — Traffic Trend Table** *(= the summary table you wanted beside the chart)*
- Visual type: **Matrix** (or Table).
- Rows: `Calendar[Month-Year]` (or the Date Granularity parameter for a matching grain).
- Values: `[Total Views]`, `[Total Users]`.
- Turn on **Totals** (Format ▸ Row subtotals/Grand total) for the total row.
- Place it to the **right of Visual A** (this is trivial and reliable in Power BI — no custom fields needed).

**Visual C — Campaign Schedule (Gantt)** *(= "Campaign Schedule")*
- Best option: add the Microsoft-certified **Gantt** visual (Visualizations pane ▸ ⋯ ▸ Get more visuals ▸ "Gantt"). Then:
  - Task: `CampaignSpend[Campaign Name]`
  - Start Date: `CampaignSpend[Start Date]`; End/Duration: `[Campaign Duration (Days)]` or `CampaignSpend[End Date]`
  - Legend/Group: the **Schedule View** field parameter (so *Individual* splits each campaign into one bar per Marketing Platform; *Overlap* keeps one bar per campaign).
  - Colour by `CampaignSpend[Marketing Platform]`.
- No-custom-visual alternative: **Stacked bar chart** with Y = `Campaign Name` (and `Marketing Platform` when Individual), X = `[Campaign Duration (Days)]`, plus a transparent "offset to start" measure — but the Gantt custom visual is closest to the Tableau Gantt.

---

## 3. Page: **Dashboard 1 - Total Web Traffic**

**Slicers (top):** `Calendar[Date]` (Between), `Campaign[Campaign Name]`, `Campaign[Campaign ID]`, `Campaign[Dept/Sch/Institute]`, `WebTraffic[Page path and screen class]`.

**Visuals:**
- **KPI cards** *(= "D1 | Key Metrics")*: Card visuals for `[Total Views]`, `[Total Users]`, `[Total Sessions]`, `[Avg Session Duration (min sec)]`.
- **Graph 1 — All CET Pages (dual-axis combo)** *(= "D1 | Traffic - All CET Pages")*: Line and clustered column chart; X = Date Granularity parameter (or `Calendar[Month-Year]`); columns `[Total Views]`; line `[Total Users]`.
- **Selected Pages (line)** *(= "D1 | Traffic - Selected Pages")*: Line chart; X = date; Y = `[Total Views]`; Legend = `WebTraffic[Page path and screen class]`; use the Page-path slicer to select.
- **Page Performance table** *(= "Page Performance Details")*: Table/Matrix; Rows = `WebTraffic[Page path and screen class]` (add Campaign ID / Campaign Name if desired); Values = `[Total Views]`, `[Total Users]`, `[Avg Session Duration (min sec)]`. Add a Page-path slicer with search.

---

## 4. Page: **Dashboard 2 - Total Campaign Spends**

**Slicers (top-right):** `CampaignSpend[Campaign ID]`, `CampaignSpend[Campaign Name]`, `CampaignSpend[Dept/Sch/Institute]`, `CampaignSpend[Start Date]` (Between), and optionally `CampaignSpend[Campaign Objective]`.

**Visuals (all use CampaignSpend):**
- **Spend by Objective** — Clustered bar; Axis `Campaign Objective`; Value `[Total Spend]`; data labels on.
- **Spend by Channel** — Clustered bar; Axis `Marketing Channel`; Value `[Total Spend]`.
- **Spend – Digital Ads / Content Marketing / OOH Ads / Others** — four Clustered bars; Axis `Marketing Platform`; Value `[Total Spend]`; each filtered (Visual-level filter) to one `Marketing Channel` value. *(Or one bar chart + a `Marketing Channel` slicer.)*

---

## 5. Page: **Campaign Spending - Financial Overview**

**Visuals (CampaignSpend):**
- **KPI Banner** — Card: `[Total Spend]`.
- **Channel Mix (left, main focus)** — **Treemap**; Group = `Marketing Platform`; Values = `[Total Spend]`; add `[% of Total Spend]` to tooltips/labels (dynamic % of grand total).
- **Spend by Dept (right)** — Clustered column; Axis = `Dept/Sch/Institute`; Value = `[Total Spend]`; Legend = `Campaign Type` (different palette from Channel Mix).
- **Cost Details (matrix)** — Rows = `Campaign Name`; add `Start Date`, `End Date` right after the name; Values = `[Total Spend]` (single "Total Spend" replacing the three cost components). Optionally break down `Marketing Channel` / `Marketing Platform`.
- **Filters:** `Campaign Name` slicer; `Campaign Type` + `Campaign Objective` slicers.

---

## 6. Formatting to match version-2
- **Locale/date format:** File ▸ Options ▸ Regional settings → **English (United Kingdom)** for `DD/MM/YYYY`; the Calendar `Month-Year` shows `MMM yy`.
- **Currency:** format spend measures as `$ #,##0` (already set in the TMDL model).
- **Colours:** give Channel Mix and Spend-by-Dept different palettes (client request).
- **Marketing Platform** already shows `Print` as **Brochures** (done in Power Query).

---

## 7. Parity checklist vs Tableau version-2
- [ ] Trend chart is a dual-axis (column Views + line Users) that switches Day/Week/Month.
- [ ] Summary **table** beside the trend chart shows Views + Total users per period with a total row.
- [ ] Campaign Schedule shows one bar per Marketing Platform in *Individual*, combined in *Overlap* (Schedule View parameter).
- [ ] Date slicer filters the trend, table and schedule together.
- [ ] Spend pages: % of grand total dynamic, `Print`→`Brochures`, single "Total Spend".
- [ ] Dates render DD/MM/YYYY.

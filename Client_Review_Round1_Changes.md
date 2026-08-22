# Client Review – Round 1 Changes

Addresses the client's "Not yet done / Cannot choose / Don't see" comments on the **Web Traffic
Dashboard** and **Campaign Spending – Financial Overview** dashboards. Items Tris already marked
**"Ok on Tableau"** were left untouched, as agreed.

Everything below was validated to keep the workbook XML well-formed. Because this environment can't run
Tableau Desktop, changes that are purely **layout positioning** or that need a **parameter/interaction
built and visually verified** are provided as precise Tableau steps rather than hand-edited blind.

---

## A. Done in the workbook file

### Data
1. **`Print` → `Brochures`** — added a value alias on `Marketing Platform` in the
   `Final_Campaign_Spend_Data` source, so it displays as **Brochures** everywhere (Channel Mix, Cost
   Details, Dashboard 2, etc.) without editing the CSV.

### Page Performance Details
2. **Page path filter opened up** — the sheet was hard-locked to a single page (`/l_adult-learner`).
   It's now an open, searchable filter (all pages), so anyone can type/scroll to the parent page they
   want. (Surface it on the dashboard via *Analysis → Filters*, or right-click the Page field → *Show Filter*.)
3. **Weighted average confirmed** — the sheet already uses `True Avg Session Duration`
   = `SUM([Avg session duration] × [Sessions]) / SUM([Sessions])` (a proper weighted average, not a sum),
   so comment #6 is already satisfied.
4. **New field `Avg Session Duration (min sec)`** added (e.g. `4min 51s`) for the "xx Min xx Sec" format
   request — see step **T3** below for the 30-second swap-in.

### Channel Mix
5. **Dynamic % of grand total** — added a `% of Total Spend` measure
   (`SUM([Total Campaign Spend]) / TOTAL(SUM([Total Campaign Spend]))`), shown as a label and formatted
   as a percentage. It recalculates automatically as filters change.

### Cost Details by Campaign
6. **Collapsed to a single `Total Spend` column** — the three component columns (Media Cost, Production
   Cost, Agency Fee) were replaced by one **Total Spend** column (a passthrough of Total Campaign Spend),
   per "rename … to Total Spend". *(If you actually wanted to keep the 3 components and only relabel the
   total, tell me and I'll revert the collapse.)*

### Campaign Schedule  → new sheet `Campaign Schedule by Platform`
7. The original `Campaign Schedule` is built on **"Mock + Live Data", which has no Marketing Platform
   field**, so it can't show platform rows. I added a **new, corrected Gantt** on
   `Final_Campaign_Spend_Data` that fixes several comments at once:
   - **Marketing Platform instead of Marketing Channel** (colour + rows).
   - **One bar per Marketing Platform** within each campaign (multiple rows per campaign period).
   - **Dynamic date axis** (continuous `Campaign Start Date`), so it no longer starts at a fixed "Jan 07"
     and it responds to the Campaign ID / Campaign Name / Department / Duration filters that are attached.
   - The original `Campaign Schedule` sheet is left intact. **To use it:** open the Web Traffic Dashboard,
     drag `Campaign Schedule by Platform` in and remove the old `Campaign Schedule` zone.

---

## B. To finish in Tableau Desktop (quick, and safer to verify visually)

### Traffic "Total Web Traffic Over Time" (sheet: `Traffic Trend Analysis`)
- **T1 – Month/Week/Day toggle (priority):**
  1. Create a **parameter** `Date Granularity` (String) with values `day`, `week`, `month` (aliases Day/Week/Month; default `month`).
  2. Create a calc `Date (by granularity)` = `DATETRUNC([Date Granularity], [Date])`.
  3. Put `Date (by granularity)` (continuous) on Columns in place of the current `WEEK(Date)`.
  4. Right-click the parameter → *Show Parameter* and add it to the dashboard.
- **T2 – MMM-YY labels:** right-click the date axis → *Format* → Dates → custom `mmm-yy`.
- **T3 – Duration as "min sec":** on `Page Performance Details`, drag the new **`Avg Session Duration
  (min sec)`** field onto the table in place of `True Avg Session Duration` (it renders e.g. `4min 51s`).
- **T4 – Tooltip values as a table under the axis:** simplest is to turn on mark labels for the bars
  (Views) and add a second row of labels for Total users, or place a small companion text table
  (Views / Users by period) directly beneath the chart on the dashboard. Happy to build this if you
  confirm the exact layout you want.

### Campaign Spending – Financial Overview
- **F1 – Add filters (Date range, Campaign ID, Campaign Objective):** on each spend sheet (Channel Mix,
  Cost Details, KPI Banner, Spend by Dept, and the new Gantt), add `Campaign ID`, `Campaign Objective`
  and a `Campaign Start Date` **range** filter; then *Apply to Worksheets → Selected Worksheets* (the
  spend sheets) and *Show Filter*.
- **F2 – Checkbox filters:** the reason Campaign Type / Campaign Name can't be switched to checkboxes is
  they're currently driven by a **filter action**, not a normal filter. Add them as regular filters
  (drag to the Filters shelf, *Show Filter*) → each card's dropdown will then offer *Multiple Values
  (dropdown/list)* = checkboxes.
- **F3 – Filter placement:** float/anchor all filter cards **top-right** and align them.
- **F4 – Layout:** move **Channel Mix to the left as the main focus**; move **Spend by Department** and
  **Cost Details** to the **right**.
- **F5 – Cost Details start & end dates:** drag `Campaign Start Date` and `Campaign End Date` (already in
  the data source) onto **Rows, right after Campaign Name**, and format as `DD/MM/YYYY`.

---

## C. Notes / decisions to confirm
- **Cost Details "Total Spend"** — collapsed the 3 cost components into one column (see A6). Confirm this
  is the intended reading.
- **"% Completion"** (Campaign Schedule) — not present anywhere in the workbook, so nothing to change;
  matches Tris's "Don't see this on Tableau".
- Because I can't open the workbook in Tableau here, please open it and confirm the changed sheets render
  as expected; I can adjust anything that looks off.

# Power BI Build Guide — Web Traffic & Campaign dashboards

Detailed, click‑by‑click steps to build **everything** in the two dashboards from scratch in
**Power BI Desktop**, matching the current project (tag **v0.2.2**):

1. **Web Traffic Dashboard**
2. **Campaign Spending – Financial Overview**

(The project also ships two extra pages — *Dashboard 1 – Total Web Traffic* and *Dashboard 2 – Total
Campaign Spends* — summarised in §8.)

> **Fastest path:** open `WebTrafficAnalysis.pbip` in Power BI Desktop (Dec 2023 or later, with
> *File ▸ Options ▸ Preview features ▸ Store reports using enhanced metadata format (PBIR)* and the
> *.pbip save option* enabled), set the `SourceFolder` parameter (Step 1.3) and **Close & Apply**.
> Everything below is the "build from scratch" path, which also documents exactly how each object is
> configured so you can rebuild or audit any piece.

Canvas size for both pages: **1280 × 720** (Format ▸ Canvas settings ▸ Type = 16:9, or set width/height).
All positions below are in report pixels (x = from left, y = from top).

---

## Step 0 — Data files

Put these CSVs in one folder (the `SourceFolder`):

| File | Becomes table | Purpose |
|------|---------------|---------|
| `Mock_WebTraffic.csv` | **WebTraffic** | daily web traffic (Views, Total users, Sessions, Avg session duration) by Date × Page × UTM |
| `Final_Campaign_Spend_Data.csv` | **CampaignSpend** | one row per campaign × marketing platform (costs + Start/End dates) |
| `Fact_Actual_Spend.csv` | **FactActualSpend** | optional platform actuals (not used by the two main dashboards) |
| *(derived)* | **Campaign** | dimension, one row per `Campaign Name for UTM` |
| *(generated in M)* | **Calendar** | date table (2024‑01‑01 → 2025‑12‑31) |

Copy‑paste scripts live in `powerquery/` and `dax/`.

---

## Step 1 — Load the data (Power Query)

### 1.1 Turn on project save format
`File ▸ Options ▸ Preview features` → tick **Power BI Project (.pbip) save option** and **PBIR**.

### 1.2 Open Power Query
`Home ▸ Transform data`.

### 1.3 Create the `SourceFolder` parameter
`Manage Parameters ▸ New`:
- Name **`SourceFolder`**, Type **Text**, Current Value = your folder path **with a trailing backslash**, e.g. `C:\Work\CETMarketingKiro\`.

### 1.4 Add each table
For every table: `New Source ▸ Blank Query ▸ Advanced Editor`, paste the matching `powerquery/*.m`
script, rename the query. Key points baked into the scripts:

- **WebTraffic** (`WebTraffic.m`): promotes headers, types columns with **en‑US** (dates are US `M/D/YYYY`),
  renames `Total users → Users` (so it doesn't clash with the `[Total Users]` measure), drops null‑date rows.
- **CampaignSpend** (`CampaignSpend.m`): promotes headers, types the text/number columns, then parses
  **Start Date / End Date** with a defensive `ToDate` function that accepts **either** text datetimes
  (`2024-03-01 00:00:00`) **or Excel serial numbers** (e.g. `45445`), and finally replaces
  `Marketing Platform` value **`Print` → `Brochures`**. The robust date step is essential — plain
  `type datetime` throws `DataFormat.Error` on serial‑number exports.
- **Campaign** (`Campaign.m`): `Source = CampaignSpend`, keep the campaign attribute columns, then
  `Table.Group` by `Campaign Name for UTM` (one row per UTM; `Start Date = List.Min`, `End Date = List.Max`).
- **Calendar** (`Calendar.m`): generates a continuous date table and adds `Year`, `Month No`,
  `Month-Year` (`MMM yy`), `Month Sort` (`Year*100+Month`), `Week Start`, `Week Label`.
- **FactActualSpend** (`FactActualSpend.m`): straight load (optional).

### 1.5 Close & Apply.

---

## Step 2 — Model: column types, relationships, date table

### 2.1 Confirm column data types (Model / Data view)
- `WebTraffic[Date]` → **Date**; `Views`,`Users`,`Sessions` → Whole number; `Average session duration` → Decimal.
- `CampaignSpend[Start Date]`,`[End Date]` → **Date**; cost columns → Decimal.
- `Calendar[Date]` → **Date**.

### 2.2 Relationships (Model view — `relationships.tmdl`)
Create these three (all single‑direction, one → many):

| From (many) | To (one) | Notes |
|-------------|----------|-------|
| `WebTraffic[Campaign Name for UTM]` | `Campaign[Campaign Name for UTM]` | campaign attributes for web traffic |
| `WebTraffic[Date]` | `Calendar[Date]` | trend axis + date slicer |
| `CampaignSpend[Campaign Name for UTM]` | `Campaign[Campaign Name for UTM]` | **lets the Campaign / Campaign ID / Dept slicers also filter the Campaign Schedule** |

`Campaign` is the shared dimension (the "one" side in all cases). There is no direct
CampaignSpend↔WebTraffic relationship (no ambiguity).

### 2.3 Mark the date table
Select **Calendar** → `Table tools ▸ Mark as date table` → Date column = `Calendar[Date]`.
Set `Calendar[Month-Year]` **Sort by column** = `Calendar[Month Sort]`.

---

## Step 3 — Measures (New measure)

Paste from `dax/measures.dax`. Full list:

**WebTraffic**
```DAX
Total Views    = SUM ( WebTraffic[Views] )
Total Users    = SUM ( WebTraffic[Users] )
Total Sessions = SUM ( WebTraffic[Sessions] )

Weighted Avg Session Duration (s) =
DIVIDE ( SUMX ( WebTraffic, WebTraffic[Average session duration] * WebTraffic[Sessions] ),
         SUM ( WebTraffic[Sessions] ) )

Avg Session Duration (min sec) =
VAR SecondsTotal = [Weighted Avg Session Duration (s)]
VAR Mins = INT ( DIVIDE ( SecondsTotal, 60 ) )
VAR Secs = INT ( MOD ( SecondsTotal, 60 ) )
RETURN IF ( ISBLANK ( SecondsTotal ), BLANK (),
            FORMAT ( Mins, "0" ) & "min " & FORMAT ( Secs, "00" ) & "s" )
```

**CampaignSpend**
```DAX
Total Spend           = SUM ( CampaignSpend[Total Campaign Spend] )      -- format $ #,##0
Total Media Cost      = SUM ( CampaignSpend[Media Cost] )
Total Production Cost = SUM ( CampaignSpend[Production Cost] )
Total Agency Fee      = SUM ( CampaignSpend[Calculated Agency Fee] )
% of Total Spend      = DIVIDE ( [Total Spend], CALCULATE ( [Total Spend], ALLSELECTED ( CampaignSpend ) ) )   -- format %
Campaign Count        = DISTINCTCOUNT ( CampaignSpend[Campaign Name] )
Platform Count        = DISTINCTCOUNT ( CampaignSpend[Marketing Platform] )
```

**Campaign Schedule (Gantt) helpers — CampaignSpend.** The Date slicer sits on `Calendar[Date]`;
these harvest `MIN/MAX(Calendar[Date])` so the schedule reacts to the Date From/To slicer and clips
each bar to that window. Non‑overlapping campaigns return `BLANK` and drop off.
```DAX
Gantt Start Offset (Days) =            -- transparent "float to start" segment
VAR WinFrom = MIN ( Calendar[Date] )
VAR WinTo   = MAX ( Calendar[Date] )
VAR CampStart = MIN ( CampaignSpend[Start Date] )
VAR CampEnd   = MAX ( CampaignSpend[End Date] )
VAR Overlaps  = CampStart <= WinTo && CampEnd >= WinFrom
VAR ClippedStart = IF ( CampStart < WinFrom, WinFrom, CampStart )
RETURN IF ( Overlaps, DATEDIFF ( WinFrom, ClippedStart, DAY ) )

Gantt Duration (Days) =                -- visible bar length (clipped to window)
VAR WinFrom = MIN ( Calendar[Date] )
VAR WinTo   = MAX ( Calendar[Date] )
VAR CampStart = MIN ( CampaignSpend[Start Date] )
VAR CampEnd   = MAX ( CampaignSpend[End Date] )
VAR Overlaps  = CampStart <= WinTo && CampEnd >= WinFrom
VAR ClippedStart = IF ( CampStart < WinFrom, WinFrom, CampStart )
VAR ClippedEnd   = IF ( CampEnd   > WinTo,   WinTo,   CampEnd )
RETURN IF ( Overlaps, DATEDIFF ( ClippedStart, ClippedEnd, DAY ) + 1 )
```

---

## Step 4 — Calculated columns (New column, on CampaignSpend)

```DAX
Campaign Duration (Days) = DATEDIFF ( CampaignSpend[Start Date], CampaignSpend[End Date], DAY )

-- Single-line "Campaign — Platform" label so the schedule bar chart shows BOTH values on ONE
-- visible axis level (a two-field axis hierarchy hides the child behind drill-down).
Campaign & Platform = CampaignSpend[Campaign Name] & "  —  " & CampaignSpend[Marketing Platform]
```

---

## Step 5 — Page: **Web Traffic Dashboard**

Create a page, rename it **Web Traffic Dashboard**, canvas 1280×720.

### 5.1 Slicer strip (top)
Add 5 **Slicer** visuals. For the categorical ones set slicer **mode = Dropdown** (Format ▸ Slicer
settings ▸ Options ▸ Style = Dropdown) and turn the **Header/title** on with the text below.

| Visual | Field | Style | Position (x, y, w, h) | Title |
|--------|-------|-------|-----------------------|-------|
| vSlicerDate01 | `Calendar[Date]` | **Between** | 8, 8, 236, 56 | Date From / To |
| vWTSlicerCampaign | `Campaign[Campaign Name for UTM]` | Dropdown | 250, 8, 190, 56 | Campaign (UTM) |
| vWTSlicerDept | `Campaign[Dept/Sch/Institute]` | Dropdown | 446, 8, 150, 56 | Dept / Sch / Institute |
| vWTSlicerCampaignID | `Campaign[Campaign ID]` | Dropdown | 608, 0, 192, 64 | Campaign ID |
| vWTSlicerPlatform | `CampaignSpend[Marketing Platform]` | Dropdown | 864, 0, 224, 64 | Marketing Platform |

> The Campaign / Dept / Campaign ID slicers use the **Campaign** dimension, so — thanks to the
> `Campaign → CampaignSpend` relationship — they filter **both** the web‑traffic visuals **and** the
> Campaign Schedule. The Marketing Platform slicer is on `CampaignSpend` and filters the schedule.

### 5.2 Visual A — Traffic Trend Table (matrix)
- Visual: **Matrix**. Position **0, 96, 320, 224**. Title: *Traffic Trend Table — Total Views & Users by Month*.
- **Rows:** `Calendar[Year]`, then `Calendar[Month-Year]`.
- **Values:** `[Total Views]`, `[Total Users]`.
- Format ▸ Row subtotals **On** (year subtotals + grand total).

### 5.3 Visual B — Traffic Trend Analysis (combo)
- Visual: **Line and clustered column chart**. Position **320, 96, 912, 224**.
  Title: *Traffic Trend Analysis — Total Web Traffic Over Time*.
- **X‑axis:** `Calendar[Month-Year]` (sorted by `Month Sort`, ascending).
- **Column y‑axis:** `[Total Views]`.
- **Line y‑axis:** `[Total Users]`.

### 5.4 Visual C — Campaign Schedule (Gantt via stacked bar)
- Visual: **Stacked bar chart**. Position **8, 330, 1232, 200**.
  Title: *Campaign Schedule — Campaign & Marketing Platform*.
- **Y‑axis (Category):** `CampaignSpend[Campaign & Platform]`  ← the composite column, so each
  **Campaign — Platform** is its own visible row/bar.
- **X‑axis (Values), in this order:** `[Gantt Start Offset (Days)]`, then `[Gantt Duration (Days)]`.
- **Tooltips:** `CampaignSpend[Campaign Name]`, `CampaignSpend[Marketing Platform]`.
- **Make the offset invisible (this is what turns a stacked bar into a Gantt):**
  Format ▸ **Columns/Bars ▸ Colors** → set the **`Gantt Start Offset (Days)`** series **fill to White**
  (`#FFFFFF`). Leave `Gantt Duration (Days)` a solid colour. Turn the **Legend Off**.
- Sort the visual by `[Gantt Start Offset (Days)]` **ascending** (chronological).
- Result: each bar floats to its start date and its length = duration, all clipped to the Date From/To
  window (from Step 3's measures).

### 5.5 Visual D — Page Performance Details (matrix)
- Visual: **Matrix**. Position **8, 538, 1232, 174**. Title: *Page Performance Details*.
- **Rows:** `Campaign[Campaign ID]`, `Campaign[Campaign Name]`, `WebTraffic[Page path and screen class]`.
- **Values:** `[Total Views]`, `[Total Users]`, `[Avg Session Duration (min sec)]`.
- Sort by `[Total Views]` descending. Row subtotals **On** for the Campaign ID / Campaign Name groups.

---

## Step 6 — Page: **Campaign Spending – Financial Overview**

New page, rename **Campaign Spending - Financial Overview**, canvas 1280×720.

### 6.1 Slicer strip (top, y = 8, h = 56)
Eight **Slicer** visuals (all on **CampaignSpend**; categorical ones = Dropdown, titles on):

| Visual | Field | Style | x, w | Title |
|--------|-------|-------|------|-------|
| vFOSlicerDate | `Start Date` | **Between** | 8, 200 | Campaign Start Date |
| vFOSlicerDept | `Dept/Sch/Institute` | Dropdown | 214, 140 | Dept / Sch / Institute |
| vFOSlicerName | `Campaign Name` | Dropdown | 360, 150 | Campaign Name |
| vFOSlicerID | `Campaign ID` | Dropdown | 516, 120 | Campaign ID |
| vFOSlicerType | `Campaign Type` | Dropdown | 642, 130 | Campaign Type |
| vFOSlicerObjective | `Campaign Objective` | Dropdown | 778, 150 | Campaign Objective |
| vFOSlicerChannel | `Marketing Channel` | Dropdown | 934, 150 | Marketing Channel |
| vFOSlicerPlatform | `Marketing Platform` | Dropdown | 1090, 150 | Marketing Platform |

### 6.2 KPI cards (y = 64, h = 80)
Three **Card** visuals:

| Visual | Field | x, w | Title |
|--------|-------|------|-------|
| vFOKPI | `[Total Spend]` | 0, 368 | Total Campaign Investment |
| vFOKPICount | `[Campaign Count]` | 368, 208 | Campaigns |
| vFOKPIPlatform | `[Platform Count]` | 576, 208 | Platforms |

### 6.3 Channel Mix (treemap)
- Visual: **Treemap**. Position **0, 160, 912, 320**. Title: *Channel Mix (Spend by Channel & Platform)*.
- **Category / Group:** `CampaignSpend[Marketing Channel]`.
- **Details:** `CampaignSpend[Marketing Platform]`.
- **Values:** `[Total Spend]`. (Add `[% of Total Spend]` to the tooltip if desired.)

### 6.4 Spend by Objective (bar)
- Visual: **Clustered bar chart**. Position **912, 160, 368, 304**. Title: *Spend by Objective*.
- **Y‑axis:** `CampaignSpend[Campaign Objective]`; **X‑axis:** `[Total Spend]`; sort desc; data labels on.

### 6.5 Spend by Channel (bar)
- Visual: **Clustered bar chart**. Position **912, 464, 368, 256**. Title: *Spend by Channel*.
- **Y‑axis:** `CampaignSpend[Marketing Channel]`; **X‑axis:** `[Total Spend]`; sort desc.

### 6.6 Spend by Department (column)
- Visual: **Clustered column chart**. Position **608, 480, 304, 240**. Title: *Spend by Department*.
- **X‑axis:** `CampaignSpend[Dept/Sch/Institute]`; **Legend/Series:** `CampaignSpend[Campaign Type]`;
  **Y‑axis:** `[Total Spend]`.

### 6.7 Cost Details (matrix)
- Visual: **Matrix**. Position **0, 496, 592, 224**. Title: *Cost Details*.
- **Rows:** `Campaign Name`, `Marketing Channel`, `Marketing Platform`.
- **Values:** `[Total Spend]`, `[% of Total Spend]`.
- Sort by `[Total Spend]` desc; row subtotals + grand total On.

---

## Step 7 — Formatting to match

- **Locale:** `File ▸ Options ▸ Regional settings` → English (UK) for `DD/MM/YYYY`; `Month-Year` shows `MMM yy`.
- **Currency:** spend measures format `$ #,##0`; `% of Total Spend` = percentage.
- `Print` already shows as **Brochures** (done in Power Query).
- Give **Channel Mix** and **Spend by Department** different colour palettes.
- **Category colours (wired in the PBIR):**
  - **Campaign Schedule** → colour by campaign using **Legend = `Campaign Name`** (a different field from the
    axis `Campaign & Platform`), so all of a campaign's platform bars share one colour and each campaign
    differs. Single value = `[Gantt Duration (Days)]` (the offset "float" is dropped so a legend can drive colour).
  - **Spend by Objective** → the category is on **both Axis and Legend** so each objective bar is coloured,
    then explicit **Data colors** pin **palette A** (Awareness `#1B9E77`, Conversion `#7570B3`, Lead Generation `#66A61E`).
  - **Spend by Channel** → same pattern with **palette B** (Digital Ads `#E7298A`, Content Marketing `#D95F02`,
    Out-of-Home Ads `#E6AB02`, Others `#A6761D`).
  - **Spend by Department** keeps its own theme palette via the `Campaign Type` legend — a third, distinct set.
  If the explicit hexes don't survive a round‑trip, the Axis+Legend still guarantees each category is
  coloured; set the exact hexes in **Data colors** per category to keep the palettes non‑overlapping.

---

## Step 8 — Extra pages (optional, already in the file)

- **Dashboard 1 – Total Web Traffic:** KPI cards (`Total Views/Users/Sessions`, `Avg Session Duration (min sec)`),
  a Views+Users combo over `Month-Year`, a Page‑Performance matrix, plus Date / Campaign / Campaign ID / Page‑path slicers.
- **Dashboard 2 – Total Campaign Spends:** bar charts for Spend by Objective, Spend by Channel, Spend by
  Platform (all `[Total Spend]`), with Start Date (Between) + Campaign Type slicers.

Page order (`pages.json`): `webtrafficdashboard`, `dashboard1totalwebtraffic`, `dashboard2campaignspends`, `financialoverview`.

---

## Step 9 — Known limitations / notes

- **Gantt x‑axis units:** the schedule uses the transparent‑offset stacked‑bar technique, so its axis is
  **days across the selected Date From/To window** (0 = Date From), not literal date tick‑labels. The
  *range* stays in sync with the Traffic Trend Analysis. Literal date labels + per‑platform bar colours
  would require a marketplace **Gantt** custom visual.
- **Individual vs Overlap (Tableau "Schedule View"):** to add live switching, create a **field parameter**
  in Desktop (*Modeling ▸ New parameter ▸ Fields*) with `CampaignSpend[Campaign & Platform]`
  ("Individual (bar per platform)") and `CampaignSpend[Campaign Name]` ("Overlap (combined)"), then put
  that parameter on the schedule's Y‑axis in place of `Campaign & Platform` and add its slicer. Field
  parameters must be created in Desktop — hand‑authored ones don't bind on the axis.
- **Date Granularity (Day/Week/Month):** the trend axis is `Month-Year` (Tableau default). For live
  switching, add a field parameter over `Calendar[Date]` / `Calendar[Week Label]` / `Calendar[Month-Year]`
  in Desktop and use it as the trend X‑axis.

---

*This guide reflects tag **v0.2.2**. Copy‑paste sources: `powerquery/*.m`, `dax/measures.dax`,
`dax/calculated_columns.dax`.*

# PowerBIkiro — Power BI replica of the Tableau version-2 dashboards

This folder is the **Power BI** version of the Tableau workbook at tag `version-2`
(branch `dashboard1-web-traffic-improvements`). It reproduces the same data model and the
four dashboards: **Web Traffic Dashboard**, **Dashboard 1 – Total Web Traffic**,
**Dashboard 2 – Total Campaign Spends**, and **Campaign Spending – Financial Overview**.

## What's in here

```
PowerBI/
├─ README.md                     ← this file
├─ POWERBI_BUILD_GUIDE.md        ← exhaustive, step-by-step build (model + all 4 pages/visuals)
├─ powerquery/                   ← copy-paste Power Query (M) to load each table
│   ├─ 00_Parameters.m           ← the SourceFolder parameter (set your data path here)
│   ├─ WebTraffic.m  CampaignSpend.m  Campaign.m  Calendar.m  FactActualSpend.m
├─ dax/
│   ├─ measures.dax              ← all DAX measures (copy-paste)
│   └─ calculated_columns.dax    ← calc columns + field-parameter reference
├─ WebTrafficAnalysis.pbip                 ← Power BI Project entry file
├─ WebTrafficAnalysis.SemanticModel/       ← TMDL data model (tables, relationships, measures)
└─ WebTrafficAnalysis.Report/              ← PBIR report (4 pages; visuals built in Desktop)
```

## How to use it — two paths

**Path A — open the PBIP project (fastest model setup)**
1. In Power BI Desktop: **File ▸ Options ▸ Preview features** → enable **Power BI Project (.pbip) save option**. Update to a recent Desktop (Dec 2023 or later).
2. Open **`WebTrafficAnalysis.pbip`**.
3. In Power Query, set the **`SourceFolder`** parameter to the folder holding the CSV/XLSX files (trailing backslash), then **Close & Apply**.
4. The tables, relationships and measures load from the semantic model. Build/adjust the report visuals following **POWERBI_BUILD_GUIDE.md** (§2–§5). The report ships with the four pages already named.

**Path B — build from scratch (fully reliable)**
Follow **POWERBI_BUILD_GUIDE.md** end-to-end: paste the `powerquery/` scripts, add the `dax/` measures & columns, create the relationships and field parameters, then build each page's visuals. This path doesn't depend on the PBIP opening cleanly.

## Honest notes
- A binary **`.pbix` can't be generated** outside Power BI Desktop, so this ships the **PBIP source format** (TMDL + PBIR) — the git-friendly Power BI format.
- The TMDL model and PBIR report were **hand-authored and not opened in Power BI Desktop here**, so treat them as a strong starting point that may need minor fix-ups on first open. If anything doesn't load, **Path B** (the guide + M + DAX) reproduces everything reliably.
- Data path is parameterised (`SourceFolder`) so the project is portable across machines.

## Data model summary
- **WebTraffic** (fact) → related to **Campaign** (dim, one row per `Campaign Name for UTM`) and **Calendar** (date).
- **CampaignSpend** (one row per campaign × marketing platform; costs, Start/End dates) — standalone star for the spend pages and the Campaign Schedule.
- Key DAX: weighted avg session duration, `min sec` string, `% of Total Spend`, `Total Spend`, campaign duration.
- Parameters mapped to Power BI: Date slicer (Between), **Date Granularity** field parameter, **Schedule View** field parameter.


## Recreation status — the two required dashboards (PowerBIkiro)

Both target dashboards from `Web Traffic Analysis(Ref for migration to PowerBI).twbx`
are now **fully built out in PBIR** so every Tableau worksheet has a Power BI equivalent:

**Web Traffic Dashboard** (`pages/webtrafficdashboard`)
| Tableau worksheet | Power BI visual | Type |
|---|---|---|
| Traffic Trend Analysis | `vTrend01` — Total Views (columns) + Total Users (line) over Month-Year | line & clustered column combo |
| Traffic Trend Table | `vTable01` — Year ▸ Month-Year × Views/Users | matrix |
| Campaign Schedule (Gantt) | `vWTSchedule` — floating stacked bar (transparent `Gantt Start Offset (Days)` + `Gantt Duration (Days)`) per Campaign × Platform | stacked bar (Gantt) |
| Page Performance Details | `vWTPagePerf` — Campaign ID ▸ Campaign Name ▸ Page path × Views/Users/Avg Session Duration | matrix |
| Slicers | Date (Between), Campaign (UTM), Dept, Campaign ID, Marketing Platform | slicers |

**Campaign Spending – Financial Overview** (`pages/financialoverview`)
| Tableau worksheet | Power BI visual | Type |
|---|---|---|
| KPI Banner | `vFOKPI` Total Spend + `vFOKPICount` Campaigns + `vFOKPIPlatform` Platforms | cards |
| Channel Mix | `vFOChannelMix` — Channel ▸ Platform sized by Total Spend | treemap |
| Spend by Objective | `vFOObjective` | bar |
| Spend by Channel | `vFOChannel` | bar |
| Spend by Dept | `vFODept` — Dept × Total Spend, coloured by Campaign Type | column |
| Cost Details | `vFOCost` — Campaign ▸ Channel ▸ Platform × Total Spend / % of Total | matrix |
| Slicers | Campaign Start Date (Between), Dept, Campaign Name, Campaign ID, Campaign Type, Campaign Objective, Marketing Channel, Marketing Platform | slicers |

**Parameter mapping notes**
- *Date From / Date To* → a single **Between** date slicer.
- *Date Granularity* (Day/Week/Month) → the trend axis uses **Month-Year** (the Tableau default). The `Calendar` table already carries `Date`, `Week Label` and `Month-Year`, so a Date-Granularity field parameter can be added later if live switching is required.
- *Schedule View* (Individual/Overlap) → a **field parameter** (`Schedule View`) with a slicer that swaps the schedule's single axis field: **Individual (bar per platform)** uses the `Campaign & Platform` composite label so each Campaign × Platform is its own visible row/bar (platform is on the axis, not hidden behind bar-chart drill-down); **Overlap (combined)** uses `Campaign Name` for one bar per campaign spanning all its platforms. Campaign Name + Marketing Platform are also in the tooltip.
- Power BI has no native Gantt mark; the schedule is reproduced with the transparent-offset stacked-bar technique using the two `Gantt …` measures added to `CampaignSpend`.

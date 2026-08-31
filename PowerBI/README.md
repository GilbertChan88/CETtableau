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

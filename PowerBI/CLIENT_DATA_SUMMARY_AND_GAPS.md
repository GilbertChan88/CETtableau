# Client Data Summary & Data Requirements (Dashboards 3 & 5)

Analysis of the client‑provided `RawData/` folder (on `main`), plus the exact data still
required to build **Dashboard 3 (Overall Campaign Summary)** and **Dashboard 5 (Campaign
Performance by Content Marketing)**.

---

## Part A — Summary of what the client provided

All files sit under `RawData/`. In short, the client supplied **digital‑ads platform data**,
**CET website analytics (GA)**, and a **campaign master** — across **two campaign waves**:

- **Wave 1 — GroupM "NY2520"** (early 2025, ~15 Jan – 21 Mar 2025)
- **Wave 2 — IMC "NYP CET"** (late 2025, ~8 Aug – 2 Oct 2025)

### A1. Campaign master (the join key / dimension)
| File | Sheets | Key contents |
|---|---|---|
| `Campaign/NYP2025-001_Campaign_Master.xlsx` | `Legend`, `Master` | `Dept/Sch/Institute, Campaign ID, Campaign Name, Campaign Name for UTM, Campaign Type, Campaign Objective, Start Date, End Date, Marketing Channel, Marketing Platform, Remarks, Agency Rate, Media Cost, Production Cost`. Includes Digital Ads, Content Marketing and **OOH** platform rows (with spend only). This is the conformed **campaign dimension** used to filter by ID/Name/Objective/Dept/Duration. |

### A2. Digital‑ads platform performance (GroupM + IMC)
| File | Grain | Key metrics available |
|---|---|---|
| `Raw Data (GroupM)/NY2520 Meta Raw Data.csv` | per ad set / campaign | Reach, Impressions, CPM, Link clicks, CPC (per link click), CTR (link), Clicks (all), CTR (all), CPC (all), Amount spent, Post engagements, 3‑sec/ThruPlay/25‑100% video plays, Landing page views, Results/Result indicator, Start/End |
| `Raw Data (IMC)/NYP Raw Meta Campaign report.xlsx` | per ad/ad set | Reporting start/end, Campaign/Ad set/Ad name, Impressions, Link clicks, CTR (link), CPC (link), Amount spent, Reach, Post comments/reactions/saves/shares |
| `Raw Data (GroupM)/NY2520 LinkedIn Raw Data.xlsx` | per campaign/day | Start Date, Campaign Group/Name/ID, **Campaign ID**, Campaign Type, Budget, Total Spent, Reach, Impressions, Clicks, Video Views, Video Completions |
| `Raw Data (GroupM)/NY2520_SEM_Raw Data Report.xlsx` | 5 sheets (Overall/Keywords/Callout/Sitelinks/Structured Snippets) | Avg CPM, Impr., Interactions, Interaction rate, Avg cost, Cost, Clicks, **Conv. rate, Conversions**, Avg CPC, **Cost/conv (CPA)** |
| `Raw Data (IMC)/NYP Raw Google Campaign report.xlsx` | 4 sheets (Campaign/Ad group/Keyword/Asset groups) | Impr., Clicks, CTR, Avg CPC, Cost, **Conversions, Conv. rate, Cost/conv** |
| `Raw Data (GroupM)/YouTube Raw Data_2025 09 09 .xlsx` | 2 sheets (YouTube Ad / Strategy Device) | Impressions, Clicks, TrueView Views, 1st‑quartile/Mid/3rd‑quartile/Complete video views, Spends |

### A3. Website analytics (Google Analytics — CET site)
| File(s) | Grain | Key contents |
|---|---|---|
| `Campaign/GA_CET pages_Dec2024.csv` (+ `_NEW`) — Dec 2024 | per page path × first‑user campaign | Page path and screen class, First user campaign, Total/New/Active/Returning users, Views, Sessions, Views per session, **Average session duration**, Bounce rate, Exits |
| `Campaign/GA_CET pages_Jan-Apr2025.csv` (+ `_NEW`) — Jan–Apr 2025 | same | same (the `_NEW` files are the fuller extracts) |

> These GA files describe traffic to **CET's own website pages** (attributed to a campaign via
> *First user campaign*) — they are **not** publisher/placement metrics.

### A4. What is NOT in the client data
- **No STEP conversion export** (interest registrations / course signups). *(Needed for Dashboard 3.)*
- **No content‑marketing publisher performance** (Mothership, Straits Times, etc. reach/page views/time on page). *(Needed for Dashboard 5.)*
- **No OOH performance** (reach, QR‑code scans) — only OOH **spend** in the master. *(Needed for Dashboard 6.)*

### A5. Buildability impact
- **Dashboard 4 (Digital Ads):** ✅ now buildable — A2 + A1 cover Impressions, Reach (Meta/LinkedIn), Clicks, Link clicks, CTR, CPC, CPLC, CPM, Views, CPV, Conversions/Conv. rate/CPA (Google/SEM), filterable by Campaign ID/Objective/Dept/Duration via the master.
- **Dashboard 3 & 5:** ❌ still blocked — see Parts B and C.

---

## Part B — Information required to build **Dashboard 3 (Overall Campaign Summary)**

**Purpose (from mockup):** show **Total Conversions from STEP**, split into **Interest Registration**
and **Course Signup**, presented as a chart, filterable by Campaign ID / Name / Duration / Dept.

> **Interim build:** `dashboard5contentmktg` and `dashboard6oohads` pages now exist as **spend‑only views**
> (Content Marketing / OOH spend, campaigns, platforms/sites from `CampaignSpend`). The performance metrics
> below are still required to complete them; Dashboard 3 has no interim view (it has no spend proxy).

### B1. Required data source
A **STEP conversions export** (from the SkillsFuture/course‑registration platform, "STEP"),
one delivery per reporting period.

### B2. Required columns (minimum)
| Column | Type | Notes |
|---|---|---|
| **Campaign ID** *(or Campaign Name for UTM)* | text | **Join key** to `NYP2025-001_Campaign_Master`. Mandatory — must match master values. |
| **Date** (conversion/event date) | date | Enables the Duration (Date From/To) filter and trends. |
| **Conversion Type** | text | Must distinguish **`Interest Registration`** vs **`Course Signup`** (the two types in the mockup). |
| **Conversions (count)** | whole number | The metric plotted. |

### B3. Nice‑to‑have columns
- `Dept/Sch/Institute` (if not derivable from the campaign master via Campaign ID).
- `Course / Programme` name, `Conversion Value` (if a value/revenue is tracked).
- `Channel / Platform` or `UTM source/medium` (to attribute conversions to a channel).

### B4. Grain & format
- **Grain:** one row per **Campaign ID × Conversion Type × Date** (daily preferred; monthly acceptable).
- **Format:** CSV or XLSX with a single header row; dates in a single consistent format; no merged cells.

### B5. Open questions to confirm with the client
1. Is "Total Conversions" defined as **Interest Registrations + Course Signups**, or are there other STEP conversion types?
2. What is the **join key** in the STEP export — Campaign ID, UTM campaign, or a landing‑page URL? (Determines how we attribute.)
3. Are conversions **de‑duplicated** per user, and over what attribution window?
4. Which campaign wave(s) does STEP cover (NY2520 early‑2025, NYP CET late‑2025, or both)?

---

## Part C — Information required to build **Dashboard 5 (Campaign Performance by Content Marketing)**

**Purpose (from mockup):** show, by content‑marketing **publisher/platform** (Mothership, The Straits
Times, The Smart Local, Channel News Asia, AsiaOne, etc.), the metrics **Reach, Page Views, Average
Time on Page**, presented as a table, filterable by Campaign ID / Name / Duration / Dept, objective = Awareness.

### C1. Required data source
A **content‑marketing performance export** per publisher (from the agency/publishers). The current GA
files are CET‑site traffic, **not** publisher placement metrics, so a dedicated export is required.

### C2. Required columns (minimum)
| Column | Type | Notes |
|---|---|---|
| **Campaign ID** *(or Campaign Name for UTM)* | text | **Join key** to the campaign master. Mandatory. |
| **Date** (or reporting period start/end) | date | Enables Duration filter + trends. |
| **Publisher / Platform** | text | e.g. Mothership, The Straits Times, The Smart Local, CNA, AsiaOne. Should reconcile with the master's Content Marketing `Marketing Platform` values. |
| **Reach** | whole number | Unique users reached. |
| **Page Views** | whole number | Article/placement page views. |
| **Average Time on Page** | number (seconds) | State the **unit** (seconds vs mm:ss). |

### C3. Nice‑to‑have columns
- `Impressions`, `Clicks`, `CTR`, `Spend` (to add cost‑efficiency metrics like cost per view).
- `Article / Placement title / URL`, `Content format` (advertorial, listicle, video…).
- `Objective` (mockup implies Awareness) if it varies.

### C4. Grain & format
- **Grain:** one row per **Campaign ID × Publisher × Date (or placement)**.
- **Format:** CSV/XLSX, single header row, consistent date format, numeric metrics as numbers (no "1,234" text or "2m 05s" strings — provide seconds for time).

### C5. Open questions to confirm with the client
1. Are **Reach / Page Views / Average Time on Page** reported by the **publisher** (their site) or measured via **GA/UTM** on CET's landing pages? (Different sources, different meaning.)
2. Exact **publisher list** in scope and how each maps to the master's `Marketing Platform`.
3. **Average Time on Page** unit (seconds vs mm:ss) and whether it's per placement or per campaign.
4. Which campaign wave(s) content marketing ran in.

---

## Cross‑cutting requirement (applies to both, and to any future performance export)
Every new export **must carry a conformed campaign key (`Campaign ID`, ideally + `Campaign Name for UTM`)
that matches `NYP2025-001_Campaign_Master`, and a date column**. Without these, results cannot be filtered
by Campaign ID / Name / Duration / Dept or joined to the campaign attributes — which is exactly why the
digital‑ads actuals in earlier versions could not be filtered.

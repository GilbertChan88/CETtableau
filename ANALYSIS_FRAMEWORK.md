# CET Tableau Dashboard Analysis Framework

## Data Sources Identified

### 1. Mock_WebTraffic.csv (11.7 MB)
Likely contains:
- Timestamp/Date
- Page URLs
- Traffic sources
- User sessions
- Bounce rates
- Page views
- Campaign tracking parameters (UTM)

### 2. Final_Campaign_Spend_Data.csv (14.5 KB)
Likely contains:
- Campaign IDs
- Campaign names
- Spend amounts
- Date ranges
- Channel/category information

### 3. Fact_Actual_Spend.csv (2.2 KB)
Likely contains:
- Actual vs planned spend
- Variance calculations
- Budget tracking

### 4. Mock_NYP2025-001_Campaign_Master.xlsx
Master campaign file with:
- Campaign metadata
- Channel assignments
- Budget allocations
- Timeline information

## Dashboard Requirements (from branch names)

### Dashboard 1 - Web Traffic
Focus on:
- Web traffic analysis
- Campaign attribution
- Traffic source breakdown
- Time-series trends

### Dashboard 2 - Total Campaign Spends
Focus on:
- Overall spend tracking
- Budget vs actual
- Channel breakdown

### Dashboard 3 - Overall Campaign Summary
Focus on:
- Executive summary view
- KPIs across all campaigns
- Performance metrics

### Dashboard 4-6 - Channel-Specific Performance
- Digital Ads
- Content Marketing
- OOH (Out of Home) Ads

## Implementation Approach

1. Create new sheets prefixed with "p-" in the "perplexity" branch
2. Build on existing data structure
3. Implement client requirements from dashboard1-web-traffic-improvements branch

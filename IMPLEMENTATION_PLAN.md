# Perplexity Implementation Plan - CET Tableau Dashboards

## Overview
This document outlines the implementation approach for creating improved Tableau dashboards in the "perplexity" branch, with all sheets prefixed with "p-".

## Data Sources (from main branch)

### Primary Data Files
1. **Mock_WebTraffic.csv** (11.7 MB)
   - Primary web traffic dataset
   - Expected fields: timestamps, URLs, sessions, pageviews, traffic sources, campaign parameters

2. **Final_Campaign_Spend_Data.csv** (14.5 KB)
   - Campaign spending information
   - Expected fields: campaign IDs, names, spend amounts, dates, channels

3. **Fact_Actual_Spend.csv** (2.2 KB)
   - Actual vs planned spend tracking
   - Expected fields: budget, actual, variance

4. **Mock_NYP2025-001_Campaign_Master.xlsx**
   - Master campaign reference file
   - Expected fields: campaign metadata, channel assignments, timelines

## Dashboard Structure (p- prefixed sheets)

### Dashboard 1 - Web Traffic (Primary Focus)
- **p-Dashboard 1 - Web Traffic Overview**: Executive summary of web traffic KPIs
- **p-Dashboard 1 - Traffic Sources**: Breakdown by source/medium
- **p-Dashboard 1 - Campaign Attribution**: Traffic attributed to specific campaigns
- **p-Dashboard 1 - Time Series Analysis**: Trends over time with comparisons

### Dashboard 2 - Campaign Spends
- **p-Dashboard 2 - Total Campaign Spends**: Budget vs actual across all campaigns

### Dashboard 3 - Overall Summary
- **p-Dashboard 3 - Overall Campaign Summary**: Cross-channel performance metrics

### Dashboard 4-6 - Channel Specific
- **p-Dashboard 4 - Digital Ads Performance**: Digital advertising metrics
- **p-Dashboard 5 - Content Marketing Performance**: Content marketing ROI
- **p-Dashboard 6 - OOH Ads Performance**: Out-of-home advertising effectiveness

### Supporting Sheets
- **p-Data Dictionary**: Field definitions and calculations
- **p-Parameters**: User-controllable parameters
- **p-Calculations**: Custom calculated fields documentation

## Implementation Notes

### Client Requirements (from dashboard1-web-traffic-improvements branch)
*Note: Specific client requirements from Client_Review_Round1_Changes.md and Dashboard1_Review_and_Changes.md need to be incorporated here*

### Key Improvements to Implement
1. Clear campaign attribution in web traffic data
2. Improved traffic source categorization
3. Time-series trend analysis with period comparisons
4. Interactive filtering and parameters
5. Consistent color schemes and formatting
6. Performance KPIs aligned with client objectives

## Next Steps
1. Review client requirements from dashboard1-web-traffic-improvements branch
2. Map data fields from CSV files to dashboard requirements
3. Build Tableau worksheets with proper data connections
4. Implement calculated fields for KPIs
5. Create interactive dashboards with filters and parameters
6. Test and validate against client requirements

## Files to be Created
- Web_Traffic_Analysis_p.twb (main workbook with p- prefixed sheets)
- p_dashboard_documentation.md (detailed dashboard specifications)
- p_data_dictionary.md (field definitions and calculations)

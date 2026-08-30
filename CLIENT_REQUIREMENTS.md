# Client Requirements - Dashboard Updates

## 1) Web Traffic Dashboard

### Interface Updates
- ✅ Date filter formatting: DD/MM/YYYY (Ok on Tableau)
- ✅ Filters for Campaign ID, Dept/Sch/Institute, Campaign Name: Change to checkboxes (Ok on Tableau)
- ✅ Different colors for different legends (Ok on Tableau)
- ❌ Date label on top getting cut off - needs fixing

### Total Web Traffic Over Time
- ❌ Month sequence incorrect (should start from Jul 2024 as first bar on left for Jul 2024 - Mar 2025 range)
- ❌ Individual months should indicate year (MMM-YY format, e.g., "Jul-24")
- ❌ Tooltip pointers should show as table below X-axis for seamless presentation
- ❌ Add breakdown option: Month/Week (priority) and Day if possible
- ❌ Number of bars should reflect actual months (not limited to 12)

### Campaign Schedule
- ❌ Date range axis should be responsive/dynamic (not starting from "Jan 07")
- ❌ Different campaigns should appear based on date range selection
- ❌ Marketing Channel not reflecting correctly - should show multiple rows for multiple "Marketing Platform" during same campaign period
- ❌ "% Completion" - need to verify calculation and data source
- ❌ Rename "Marketing Channel" to "Marketing Platform"

### Page Performance Details
- ❌ Average Session Duration: Should be AVERAGE (sum divided by count), not SUM
- ❌ Average Session Duration format: xx Min xx Sec (e.g., "2min 25s")
- ❌ "Page path and screen class": Add include filter for parent pages

---

## 2) Campaign Spending - Financial Overview Dashboard

### Interface Updates
- ❌ Standardize filter placement (e.g., top right)
- ❌ Add missing filters: Date range and Campaign ID
- ❌ Change Campaign Type and Campaign Name filters to checkboxes
- ❌ Add Campaign Objective filter (Awareness/Conversion/Lead Gen)
- ✅ Different colors within same dashboard allowed (Ok on Tableau)

### Spend by Department
- ❌ Shift to the right

### Channel Mix
- ❌ Shift to the left and make it the main focus
- ❌ Change "Prints" to "Brochures" (data-level change)
- ❌ Show dynamic % of grand total
- ✅ Show total spends in $ for each category (Ok on Tableau)

### Cost Details by Campaign
- ❌ Shift to the right
- ❌ Include campaign start & end date (right after campaign name)
- ❌ Rename "Total Media Cost, Total Production Cost and Total Agency Fee" to "Total Spend"

---

## Implementation Priority

### High Priority (Not yet done on Tableau)
1. Date formatting and labeling (MMM-YY)
2. Time breakdown options (Month/Week/Day)
3. Campaign Schedule dynamic date range
4. Marketing Platform multi-row display
5. Average Session Duration calculation and formatting
6. Filter standardization and additions
7. Dashboard layout reorganization

### Already OK on Tableau
- Date filter DD/MM/YYYY format
- Checkbox filters
- Different colors for legends
- Total spends in $ display

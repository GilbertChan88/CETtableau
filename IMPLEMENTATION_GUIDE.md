# Tableau Implementation Guide - Client Requirements

## Web Traffic Dashboard (Dashboard 1)

### 1. Date Label Fix (Top Getting Cut Off)
**Issue:** Date label on top getting cut off

**Solution:**
- Right-click on the date axis → Format
- Under "Header", adjust the font size or row height
- Alternatively, move the date label to a different position
- Ensure worksheet has sufficient height in dashboard

---

### 2. Date Formatting (DD/MM/YYYY)
**Status:** ✅ Already OK on Tableau

**Implementation:**
- Right-click on Date field → Format
- Under "Dates", select custom format: `dd/mm/yyyy`
- Or use calculated field: `FORMAT([Date], "dd/MM/yyyy")`

---

### 3. Checkbox Filters (Campaign ID, Dept/Sch/Institute, Campaign Name)
**Status:** ✅ Already OK on Tableau

**Implementation:**
- Add filter to dashboard
- Right-click on filter → Customize
- Select "Show Apply button" if needed
- Ensure "Multiple values (list)" is selected (not "Single value (list)")

---

### 4. Different Colors for Different Legends
**Status:** ✅ Already OK on Tableau

**Implementation:**
- Drag dimension to Color shelf
- Edit Colors → Choose appropriate palette
- Ensure "Assign palette" is set correctly

---

### 5. Month Sequence (Chronological Order)
**Issue:** Months not in correct order (e.g., Jul 2024 - Mar 2025 should start from Jul 2024)

**Solution:**
- Ensure Date field is set as continuous (green pill)
- Right-click on date pill → Format
- Under "Dates", set to "Months" with year included
- Sort by Date field ascending
- Use: `DATETRUNC('month', [Date])` for proper sorting

---

### 6. Month Labels (MMM-YY Format)
**Issue:** Individual months should indicate year (e.g., "Jul-24")

**Solution:**
- Create calculated field:
  ```
  FORMAT(DATETRUNC('month', [Date]), "MMM-YY")
  ```
- Or use custom date format on axis:
  - Right-click axis → Format
  - Dates → Custom: `MMM-YY`

---

### 7. Time Breakdown Parameter (Month/Week/Day)
**Issue:** Need breakdown by Month (default), Week (priority), or Day

**Solution:**
1. Create parameter:
   - Name: "Time Granularity"
   - Data type: String
   - Current value: "Month"
   - Allowable values: List: Month, Week, Day

2. Create calculated field:
   ```
   CASE [Time Granularity]
     WHEN 'Month' THEN DATETRUNC('month', [Date])
     WHEN 'Week' THEN DATETRUNC('week', [Date])
     WHEN 'Day' THEN [Date]
   END
   ```

3. Use this calculated field on Columns/Rows shelf
4. Show parameter control on dashboard

---

### 8. Tooltip as Table Below X-Axis
**Issue:** Tooltip pointers should show as table below X-axis

**Solution:**
- This requires a combined chart approach
- Create dual-axis chart with bar and line
- Format tooltips to show in table format
- Alternatively, create a separate crosstab sheet below the chart
- Use dashboard actions to sync highlighting

---

### 9. Dynamic Bar Count (Not Limited to 12)
**Issue:** Number of bars doesn't reflect if more than 12 months

**Solution:**
- Ensure "Fixed" is not selected for axis range
- Right-click axis → Edit Axis
- Uncheck "Fixed number of ticks"
- Set to automatic or appropriate range

---

### 10. Campaign Schedule - Dynamic Date Range
**Issue:** Date range axis should be responsive (not starting from "Jan 07")

**Solution:**
- Use context filters for date range
- Right-click date filter → Add to Context
- This makes other filters respect the date selection
- Ensure Gantt chart uses filtered data

---

### 11. Multiple Marketing Platforms Per Campaign
**Issue:** Should show multiple rows for multiple Marketing Platforms during same campaign

**Solution:**
- Ensure data has one row per campaign-platform combination
- Use Marketing Platform as a dimension in rows
- Create Gantt chart with:
  - Rows: Campaign Name, Marketing Platform
  - Columns: Start Date, End Date (or Duration)
  - Color: Marketing Platform

---

### 12. Rename "Marketing Channel" to "Marketing Platform"
**Solution:**
- Rename field in data source
- Or create alias:
  - Right-click on field → Aliases
  - Change "Marketing Channel" to "Marketing Platform"
- Update all references in worksheets

---

### 13. Average Session Duration Calculation
**Issue:** Should be AVERAGE (sum divided by count), not SUM

**Solution:**
- Change aggregation from SUM to AVG:
  - Click on pill → Measure → Average
  - Or create calculated field: `AVG([Session Duration])`

---

### 14. Average Session Duration Format (xx Min xx Sec)
**Issue:** Should display as "2min 25s"

**Solution:**
- Create calculated field:
  ```
  STR(INT(AVG([Session Duration]) / 60)) + "min " + 
  STR(INT(AVG([Session Duration]) % 60)) + "s"
  ```
- Or format using custom number format if in seconds

---

### 15. Page Path Filter (Include Filter for Parent Pages)
**Issue:** Need searchable filter for page paths

**Solution:**
- Add Page Path to filters
- Right-click filter → Customize
- Select "Wildcard" match
- Or use parameter with CONTAINS calculation:
  ```
  CONTAINS([Page Path], [Page Path Search])
  ```

---

## Campaign Spending Dashboard (Dashboard 2)

### 16. Standardize Filter Placement (Top Right)
**Solution:**
- In dashboard, drag all filters to top right container
- Use horizontal layout container
- Align filters consistently

---

### 17. Add Missing Filters (Date Range, Campaign ID)
**Solution:**
- Add Date filter:
  - Drag Date field to Filters shelf
  - Select date range option
  - Show filter on dashboard

- Add Campaign ID filter:
  - Drag Campaign ID to Filters shelf
  - Show filter on dashboard

---

### 18. Checkbox Filters (Campaign Type, Campaign Name)
**Solution:**
- Right-click on filter → Customize
- Select "Multiple values (list)"
- Uncheck "Show Apply button" for instant filtering

---

### 19. Add Campaign Objective Filter
**Solution:**
- Create Campaign Objective dimension if not exists:
  - Values: Awareness, Conversion, Lead Gen
- Add to Filters shelf
- Show filter on dashboard (top right)

---

### 20. Channel Mix - Main Focus (Left Position)
**Solution:**
- In dashboard, drag Channel Mix sheet to left side
- Make it larger than other sheets
- Use layout containers for precise positioning

---

### 21. Rename "Prints" to "Brochures"
**Solution:**
- In data source, rename value:
  - Right-click on "Prints" → Aliases
  - Change to "Brochures"
- Or create calculated field:
  ```
  CASE [Channel]
    WHEN 'Prints' THEN 'Brochures'
    ELSE [Channel]
  END
  ```

---

### 22. Dynamic % of Grand Total
**Solution:**
- Right-click on measure in view → Quick Table Calculation → Percent of Total
- Or create calculated field:
  ```
  SUM([Spend]) / TOTAL(SUM([Spend]))
  ```
- Format as percentage

---

### 23. Campaign Start & End Date Display
**Solution:**
- Create calculated field:
  ```
  [Campaign Name] + " (" + 
  FORMAT([Start Date], "MMM dd, yyyy") + " - " + 
  FORMAT([End Date], "MMM dd, yyyy") + ")"
  ```
- Use this field in place of Campaign Name

---

### 24. Rename Cost Fields to "Total Spend"
**Solution:**
- Create calculated field:
  ```
  [Total Media Cost] + [Total Production Cost] + [Total Agency Fee]
  ```
- Name it "Total Spend"
- Use this in all visualizations
- Update field captions in views

---

## Data Preparation Notes

### For "Brochures" rename:
Ensure the data source has the correct value, or create a calculated field to transform it.

### For Campaign Objective:
If not in current data, may need to:
- Add to CSV file
- Create mapping table
- Use calculated field based on campaign type

### For % Completion:
Verify calculation:
```
% Completion = [Actual Spend] / [Planned Budget] * 100
```
Check if Planned Budget exists in data source.

---

## Testing Checklist

- [ ] All date labels show MMM-YY format
- [ ] Month sequence is chronological
- [ ] Time breakdown parameter works (Month/Week/Day)
- [ ] All filters are checkboxes (not radio buttons)
- [ ] Filters positioned at top right
- [ ] Channel Mix is main focus (left side)
- [ ] "Brochures" appears instead of "Prints"
- [ ] Average Session Duration shows as "Xmin Ys"
- [ ] Campaign Schedule Campaign Schedule shows multiple platforms per campaign
- [ ] Total Spend calculated correctly
- [ ] All colors are distinct for different categories

// ============================================================================
// Power Query PARAMETER:  SourceFolder
// ----------------------------------------------------------------------------
// Create this as a Power Query *parameter* (Home > Manage Parameters > New) of
// type Text. Set its Current Value to the folder that contains the source
// files, WITH a trailing backslash.
//
// Current default value:
//     C:\Work\CETMarketingKiro\
//
// Files expected in that folder:
//   - Mock_WebTraffic.csv
//   - Final_Campaign_Spend_Data.csv
//   - Fact_Actual_Spend.csv
//   - Mock_NYP2025-001_Campaign_Master.xlsx   (optional; "Master" sheet)
// ============================================================================

"C:\Work\CETMarketingKiro\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]

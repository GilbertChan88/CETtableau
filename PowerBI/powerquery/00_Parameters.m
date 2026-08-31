// ============================================================================
// Power Query PARAMETER:  SourceFolder
// ----------------------------------------------------------------------------
// Create this as a Power Query *parameter* (Home > Manage Parameters > New) of
// type Text. Set its Current Value to the folder that contains the source
// files, WITH a trailing backslash, e.g.:
//
//     C:\Users\<you>\CETtableau\
//
// Every table query below references [SourceFolder] so the project stays
// portable — you only change the path in one place.
//
// Files expected in that folder:
//   - Mock_WebTraffic.csv
//   - Final_Campaign_Spend_Data.csv
//   - Fact_Actual_Spend.csv
//   - Mock_NYP2025-001_Campaign_Master.xlsx   (optional; "Master" sheet)
// ============================================================================

"C:\Users\CHANGE_ME\CETtableau\" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]

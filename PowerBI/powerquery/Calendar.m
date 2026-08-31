// Query: Calendar   (date dimension for the trend axis + Day/Week/Month switching)
// Covers the data range; adjust the start/end if your data grows.
let
    StartDate = #date(2024, 1, 1),
    EndDate   = #date(2025, 12, 31),
    Days   = Duration.Days(EndDate - StartDate) + 1,
    Dates  = List.Dates(StartDate, Days, #duration(1, 0, 0, 0)),
    Table0 = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    Typed  = Table.TransformColumnTypes(Table0, {{"Date", type date}}),
    Added  = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
    Added2 = Table.AddColumn(Added, "Month No", each Date.Month([Date]), Int64.Type),
    // "Jul 24" style label; sort key keeps chronological order
    Added3 = Table.AddColumn(Added2, "Month-Year", each Date.ToText([Date], "MMM yy"), type text),
    Added4 = Table.AddColumn(Added3, "Month Sort", each Date.Year([Date]) * 100 + Date.Month([Date]), Int64.Type),
    Added5 = Table.AddColumn(Added4, "Week Start", each Date.StartOfWeek([Date], Day.Monday), type date),
    Added6 = Table.AddColumn(Added5, "Week Label", each "W" & Text.From(Date.WeekOfYear([Date], Day.Monday)) & " " & Text.From(Date.Year([Date])), type text)
in
    Added6

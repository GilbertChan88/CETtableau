// Query: CampaignSpend   (fact + campaign attributes, one row per campaign x marketing platform)
// Source: Final_Campaign_Spend_Data.csv
// Powers Dashboard 2 (spend) and the Campaign Schedule (has Start/End Date + Marketing Platform).
let
    Source = Csv.Document(
        File.Contents(SourceFolder & "Final_Campaign_Spend_Data.csv"),
        [Delimiter = ",", Columns = 16, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        Promoted,
        {
            {"Dept/Sch/Institute", type text},
            {"Campaign ID", type text},
            {"Campaign Name", type text},
            {"Campaign Name for UTM", type text},
            {"Campaign Type", type text},
            {"Campaign Objective", type text},
            {"Marketing Channel", type text},
            {"Marketing Platform", type text},
            {"Remarks", type text},
            {"Agency Rate", type number},
            {"Media Cost", type number},
            {"Production Cost", type number},
            {"Calculated Agency Fee", type number},
            {"Total Campaign Spend", type number}
        }
    ),
    // Robustly parse Start/End Date. The export can deliver them either as text
    // datetimes ("2024-03-01 00:00:00") or as Excel serial numbers (e.g. 45445);
    // "type datetime" chokes on the serial numbers, so parse each value defensively.
    ToDate = (v) as nullable date =>
        if v = null then
            null
        else if v is number then
            // Excel serial number (days since 1899-12-30)
            Date.From(#datetime(1899, 12, 30, 0, 0, 0) + #duration(v, 0, 0, 0))
        else
            let
                t = Text.Trim(Text.From(v)),
                n = try Number.FromText(t) otherwise null
            in
                if t = "" then null
                else if n <> null then Date.From(#datetime(1899, 12, 30, 0, 0, 0) + #duration(n, 0, 0, 0))
                else try Date.From(DateTime.FromText(t)) otherwise Date.FromText(t),
    ParsedDates = Table.TransformColumns(Typed, {{"Start Date", ToDate, type date}, {"End Date", ToDate, type date}}),
    // Client rename: "Print" -> "Brochures" (matches version-2 alias)
    Renamed = Table.ReplaceValue(ParsedDates, "Print", "Brochures", Replacer.ReplaceText, {"Marketing Platform"})
in
    Renamed

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
            {"Start Date", type datetime},
            {"End Date", type datetime},
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
    // Convert the datetime start/end to plain dates
    AsDates = Table.TransformColumnTypes(Typed, {{"Start Date", type date}, {"End Date", type date}}),
    // Client rename: "Print" -> "Brochures" (matches version-2 alias)
    Renamed = Table.ReplaceValue(AsDates, "Print", "Brochures", Replacer.ReplaceText, {"Marketing Platform"})
in
    Renamed

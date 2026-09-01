// Query: FactActualSpend   (optional — actual media performance, not used by the core version-2 pages)
// Source: Fact_Actual_Spend.csv
let
    Source = Csv.Document(
        File.Contents(SourceFolder & "Fact_Actual_Spend.csv"),
        [Delimiter = ",", Columns = 5, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(
        Promoted,
        {
            {"Campaign Name", type text},
            {"Spend", type number},
            {"Impressions", Int64.Type},
            {"Clicks", Int64.Type},
            {"Platform", type text}
        }
    )
in
    Typed

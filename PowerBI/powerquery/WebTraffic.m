// Query: WebTraffic   (fact table)
// Source: Mock_WebTraffic.csv
// Grain: one row per Date x Page path x Campaign Name for UTM
let
    Source = Csv.Document(
        File.Contents(SourceFolder & "Mock_WebTraffic.csv"),
        [Delimiter = ",", Columns = 7, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    // Date in the file is US format M/D/YYYY -> parse with en-US culture
    Typed = Table.TransformColumnTypes(
        Promoted,
        {
            {"Date", type date},
            {"Page path and screen class", type text},
            {"Campaign Name for UTM", type text},
            {"Views", Int64.Type},
            {"Total users", Int64.Type},
            {"Sessions", Int64.Type},
            {"Average session duration", type number}
        },
        "en-US"
    ),
    // Drop any rows where Date failed to parse (data-quality guard)
    Cleaned = Table.SelectRows(Typed, each [Date] <> null)
in
    Cleaned

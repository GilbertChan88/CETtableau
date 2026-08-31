// Query: Campaign   (dimension — ONE row per Campaign Name for UTM)
// Derived from CampaignSpend so the web-traffic fact can relate to campaign attributes.
// Marketing Channel/Platform are intentionally excluded here (they are many-per-UTM and
// live on the CampaignSpend table for the schedule/spend visuals).
let
    Source = CampaignSpend,
    Kept = Table.SelectColumns(
        Source,
        {
            "Campaign Name for UTM", "Campaign ID", "Campaign Name",
            "Dept/Sch/Institute", "Campaign Type", "Campaign Objective",
            "Start Date", "End Date"
        }
    ),
    // Collapse to one row per UTM (campaign-level attributes are constant within a UTM;
    // Start/End taken as min/max to be safe)
    Grouped = Table.Group(
        Kept,
        {"Campaign Name for UTM"},
        {
            {"Campaign ID", each List.First([Campaign ID]), type text},
            {"Campaign Name", each List.First([Campaign Name]), type text},
            {"Dept/Sch/Institute", each List.First([#"Dept/Sch/Institute"]), type text},
            {"Campaign Type", each List.First([Campaign Type]), type text},
            {"Campaign Objective", each List.First([Campaign Objective]), type text},
            {"Start Date", each List.Min([Start Date]), type date},
            {"End Date", each List.Max([End Date]), type date}
        }
    )
in
    Grouped

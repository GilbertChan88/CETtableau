#!/usr/bin/env python3
# Generates DUMMY / mock "Others" channel performance data for Dashboard 7
# ("Campaign Performance by Others"), following the D5/D6 dummy pattern.
# It reads the real campaign master (Final_Campaign_Spend_Data.csv), keeps the
# rows whose Marketing Channel == "Others", and fabricates monthly performance
# per "Others" sub-channel (Admail, Brochures, etc.) across each campaign's run.
# Output -> repo root Mock_Others_Performance.csv (copy into the Power BI SourceFolder).
import csv
import datetime
import os
import random

random.seed(42)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "Final_Campaign_Spend_Data.csv")
OUT = os.path.join(ROOT, "Mock_Others_Performance.csv")

# extra "Others" sub-channels to enrich the breakdown ("...Etc." in the mockup)
EXTRA_CHANNELS = ["Flyers", "EDM (Email)", "Roadshow"]


def parse_date(v):
    v = (v or "").strip()
    if v == "":
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.datetime.strptime(v, fmt).date()
        except ValueError:
            pass
    try:  # Excel serial
        return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(v))).date()
    except ValueError:
        return None


def month_starts(start, end):
    """First-of-month dates covering [start, end] inclusive."""
    if not start or not end or end < start:
        return []
    out, y, m = [], start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(datetime.date(y, m, 1))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def norm_channel(platform):
    # the model renames Print -> Brochures; keep the dummy consistent
    return "Brochures" if platform.strip().lower() == "print" else platform.strip()


rows = []
with open(SRC, newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        if r.get("Marketing Channel", "").strip() != "Others":
            continue
        cid = r.get("Campaign ID", "").strip()
        cname = r.get("Campaign Name", "").strip()
        dept = r.get("Dept/Sch/Institute", "").strip()
        obj = r.get("Campaign Objective", "").strip()
        base = norm_channel(r.get("Marketing Platform", "").strip())
        start = parse_date(r.get("Start Date"))
        end = parse_date(r.get("End Date"))
        months = month_starts(start, end) or [datetime.date(2025, 1, 1)]
        # this campaign's real Others channel + 1 extra for a richer breakdown
        channels = [base] + random.sample(EXTRA_CHANNELS, 1)
        for ch in channels:
            for m in months:
                reach = random.randint(5000, 200000)
                qr = random.randint(50, 3000)
                impressions = int(reach * random.uniform(1.5, 4.0))
                avg_session = round(random.uniform(30, 180), 1)  # seconds
                spend = round(random.uniform(2000, 20000), 2)
                rows.append([cid, cname, dept, obj, ch, m.isoformat(),
                             reach, qr, impressions, avg_session, spend])

cols = ["Campaign ID", "Campaign", "Dept/Sch/Institute", "Marketing Objective",
        "Channel", "Month", "Reach", "QR Code Scans", "Impressions",
        "Avg Session Duration (s)", "Spend"]
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    w.writerows(rows)

print("Mock_Others_Performance.csv rows:", len(rows))

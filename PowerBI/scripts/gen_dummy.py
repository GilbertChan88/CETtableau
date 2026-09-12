# Generates DUMMY/mock performance data for Dashboards 5 (Content Marketing) & 6 (OOH).
# Output CSVs go to the repo root (copy into the Power BI SourceFolder alongside the others).
import csv, random
random.seed(42)
ROOT = "."  # run from the repository root: python3 PowerBI/scripts/gen_dummy.py

# ---------------- Content Marketing ----------------
cm_campaigns = [
    ("CET B2C Campaign - Q1 2025", "C&O", "Awareness",       ["2025-01-01","2025-02-01","2025-03-01"]),
    ("NACE CET - B2B Campaign - Q1 2025", "NACE", "Conversion",["2025-02-01","2025-03-01"]),
    ("SIT CET - B2B Campaign - Q2 2025", "SIT", "Lead Generation",["2025-04-01","2025-05-01","2025-06-01"]),
    ("SBM PET Campaign - Q3 2025", "SBM", "Awareness",       ["2025-07-01","2025-08-01"]),
]
publishers = ["Mothership","The Straits Times","The Smart Local","Channel News Asia","AsiaOne"]

cm_rows = []
for camp, dept, obj, months in cm_campaigns:
    pubs = random.sample(publishers, random.randint(3,5))
    for m in months:
        for pub in pubs:
            reach = random.randint(20000, 250000)
            page_views = int(reach * random.uniform(0.06, 0.22))
            avg_time = round(random.uniform(45, 190), 1)          # seconds
            impressions = int(reach * random.uniform(1.2, 2.0))
            clicks = int(page_views * random.uniform(0.15, 0.45))
            spend = round(random.uniform(1000, 8000), 2)
            cm_rows.append([camp, dept, obj, pub, m, reach, page_views, avg_time, impressions, clicks, spend])

cm_cols = ["Campaign","Dept/Sch/Institute","Marketing Objective","Publisher","Month",
           "Reach","Page Views","Avg Time on Page (s)","Impressions","Clicks","Spend"]
with open(f"{ROOT}/Mock_ContentMarketing_Performance.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cm_cols); w.writerows(cm_rows)

# ---------------- OOH ----------------
ooh_campaigns = [
    ("CET B2C Campaign - Q1 2025", "C&O", "Awareness",        ["2025-01-01","2025-02-01","2025-03-01"]),
    ("SIT CET - B2B Campaign - Q2 2025", "SIT", "Conversion",["2025-04-01","2025-05-01"]),
    ("SBM PET Campaign - Q3 2025", "SBM", "Awareness",        ["2025-07-01","2025-08-01"]),
]
placements = [
    ("MRT Platform Screen Door","Hougang MRT Station"),
    ("MRT Platform Screen Door","Punggol MRT Station"),
    ("MRT Platform Screen Door","Jurong East MRT Station"),
    ("Bus Shelter Posters","Orchard Road"),
    ("Bus Shelter Posters","Ang Mo Kio Hub"),
    ("HDB Digital Display Panels","Toa Payoh Central"),
    ("HDB Digital Display Panels","Bedok Central"),
    ("Digital Screens (Mall)","VivoCity"),
    ("Digital Screens (Mall)","Nex Megamall"),
]
ooh_rows = []
for camp, dept, obj, months in ooh_campaigns:
    picks = random.sample(placements, random.randint(4,6))
    for m in months:
        for fmt, site in picks:
            reach = random.randint(50000, 800000)
            qr = random.randint(80, 5000)
            impressions = int(reach * random.uniform(2.0, 5.0))
            spend = round(random.uniform(5000, 30000), 2)
            avg_session = round(random.uniform(30, 180), 1)  # seconds
            ooh_rows.append([camp, dept, obj, fmt, site, m, reach, qr, impressions, spend, avg_session])

ooh_cols = ["Campaign","Dept/Sch/Institute","Marketing Objective","OOH Format","Site","Month",
            "Reach","QR Code Scans","Impressions","Spend","Avg Session Duration (s)"]
with open(f"{ROOT}/Mock_OOH_Performance.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(ooh_cols); w.writerows(ooh_rows)

print("Content Marketing rows:", len(cm_rows))
print("OOH rows:", len(ooh_rows))

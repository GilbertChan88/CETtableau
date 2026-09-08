# Normalises the client's digital-ads platform exports in RawData/ into one clean CSV
# (DigitalAds_Performance.csv) for the Power BI DigitalAdsPerf table / Dashboard 4.
# Run from the repository root:  python3 PowerBI/scripts/normalize_digitalads.py
# Sources: Meta (GroupM CSV + IMC xlsx), LinkedIn xlsx, SEM (GroupM xlsx), Google (IMC xlsx), YouTube xlsx.
# Output grain: one row per Platform x Campaign; Objective parsed from campaign name; totals rows dropped.
import zipfile, re, csv, io, datetime
import xml.etree.ElementTree as ET

RAW = "RawData"
OUT = "DigitalAds_Performance.csv"
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

def col_num(ref):
    m = re.match(r'([A-Z]+)', ref); n = 0
    for c in m.group(1): n = n*26 + (ord(c)-64)
    return n-1

def xlsx_rows(path, sheet_index=0):
    z = zipfile.ZipFile(path)
    ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        r = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in r.findall(NS+'si'):
            ss.append(''.join(t.text or '' for t in si.iter(NS+'t')))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    sheets = [(s.get('name'), s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')) for s in wb.iter(NS+'sheet')]
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rid2t = {rel.get('Id'): rel.get('Target') for rel in rels}
    name, rid = sheets[sheet_index]; tgt = rid2t[rid]
    if not tgt.startswith('xl/'): tgt = 'xl/'+tgt.lstrip('/')
    root = ET.fromstring(z.read(tgt))
    out = []
    for row in root.iter(NS+'row'):
        cells = {}
        for c in row.findall(NS+'c'):
            ref = c.get('r'); t = c.get('t'); v = c.find(NS+'v'); isv = c.find(NS+'is'); val = ''
            if t == 's' and v is not None: val = ss[int(v.text)]
            elif t == 'inlineStr' and isv is not None: val = ''.join(x.text or '' for x in isv.iter(NS+'t'))
            elif v is not None: val = v.text
            cells[col_num(ref)] = val
        mx = max(cells) if cells else -1
        out.append([cells.get(i, '') for i in range(mx+1)])
    return out

def csv_rows(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return [r for r in csv.reader(f)]

def num(v):
    if v is None: return 0.0
    s = str(v).strip().replace(',', '')
    if s in ('', '--', 'N/A'): return 0.0
    try: return float(s)
    except: return 0.0

def to_iso(v, kind):
    if v is None or str(v).strip() == '': return ''
    s = str(v).strip()
    try:
        if kind == 'serial':
            return (datetime.date(1899,12,30) + datetime.timedelta(days=int(float(s)))).isoformat()
        if kind == 'ddmmyy':  # 08-01-25
            d,m,y = s.split('-'); return datetime.date(2000+int(y), int(m), int(d)).isoformat()
        if kind == 'mdy':  # 2/28/2025
            m,d,y = s.split('/'); return datetime.date(int(y), int(m), int(d)).isoformat()
    except: return ''
    return ''

OBJ_KEYS = ['Awareness', 'Consideration', 'Conversion', 'Lead Generation', 'Traffic', 'Engagement', 'Reach']
def objective(campaign):
    parts = re.split(r'\s*[-|]\s*', str(campaign))
    for p in parts:
        for k in OBJ_KEYS:
            if p.strip().lower() == k.lower():
                return k
    low = str(campaign).lower()
    for k in OBJ_KEYS:
        if k.lower() in low:
            return k
    return '(Unspecified)'

# accumulator keyed by (platform, campaign)
acc = {}
def add(platform, campaign, impressions=0, reach=0, clicks=0, link_clicks=0, video_views=0, conversions=0, spend=0, start='', end=''):
    campaign = (campaign or '').strip()
    cl = campaign.lower()
    # skip totals / summary / empty rows
    if cl in ('', '--', '-', 'total', 'grand total', 'totals') or cl.startswith('total') or cl.startswith('grand total'):
        return
    key = (platform, campaign)
    r = acc.get(key)
    if not r:
        r = dict(Platform=platform, Campaign=campaign, Objective=objective(campaign),
                 Impressions=0.0, Reach=0.0, Clicks=0.0, LinkClicks=0.0, VideoViews=0.0,
                 Conversions=0.0, Spend=0.0, Start='', End='')
        acc[key] = r
    r['Impressions'] += num(impressions); r['Reach'] += num(reach); r['Clicks'] += num(clicks)
    r['LinkClicks'] += num(link_clicks); r['VideoViews'] += num(video_views)
    r['Conversions'] += num(conversions); r['Spend'] += num(spend)
    if start:
        r['Start'] = start if not r['Start'] else min(r['Start'], start)
    if end:
        r['End'] = end if not r['End'] else max(r['End'], end)

def hdr_index(header):
    return {h.strip(): i for i, h in enumerate(header)}

# 1) GroupM Meta CSV
rows = csv_rows(f"{RAW}/Campaign/Raw Data (GroupM)/NY2520 Meta Raw Data.csv")
h = hdr_index(rows[0])
def g(row, key):
    i = h.get(key); return row[i] if i is not None and i < len(row) else ''
for row in rows[1:]:
    if not any(row): continue
    add('Meta', g(row,'Campaign name'), impressions=g(row,'Impressions'), reach=g(row,'Reach'),
        clicks=g(row,'Clicks (all)'), link_clicks=g(row,'Link clicks'), video_views=g(row,'ThruPlays'),
        spend=g(row,'Amount spent (SGD)'), start=to_iso(g(row,'Starts'),'ddmmyy'), end=to_iso(g(row,'Ends'),'ddmmyy'))

# 2) IMC Meta xlsx
rows = xlsx_rows(f"{RAW}/Raw Data (IMC)/NYP Raw Meta Campaign report.xlsx")
h = hdr_index(rows[0])
for row in rows[1:]:
    if not any(row): continue
    add('Meta', g(row,'Campaign name'), impressions=g(row,'Impressions'), reach=g(row,'Reach'),
        link_clicks=g(row,'Link clicks'), spend=g(row,'Amount spent (SGD)'),
        start=to_iso(g(row,'Reporting starts'),'serial'), end=to_iso(g(row,'Reporting ends'),'serial'))

# 3) LinkedIn xlsx (header row 5 -> index 4)
rows = xlsx_rows(f"{RAW}/Campaign/Raw Data (GroupM)/NY2520 LinkedIn Raw Data.xlsx")
header = rows[4]; h = hdr_index(header)
for row in rows[5:]:
    if not any(row): continue
    add('LinkedIn', g(row,'Campaign Group Name'), impressions=g(row,'Impressions'), reach=g(row,'Reach'),
        clicks=g(row,'Clicks'), video_views=g(row,'Video Views'), spend=g(row,'Total Spent'),
        start=to_iso(g(row,'Start Date (in UTC)'),'mdy'))

# 4) GroupM SEM xlsx (sheet 0 = SEM_Overall Report, header row 3 -> index 2)
rows = xlsx_rows(f"{RAW}/Campaign/Raw Data (GroupM)/NY2520_SEM_Raw Data Report.xlsx", 0)
header = rows[2]; h = hdr_index(header)
for row in rows[3:]:
    if not any(row): continue
    add('Google Search', g(row,'Campaign'), impressions=g(row,'Impr.'), clicks=g(row,'Clicks'),
        conversions=g(row,'Conversions'), spend=g(row,'Cost'))

# 5) IMC Google xlsx (sheet 0 = Campaign report, header row 3 -> index 2)
rows = xlsx_rows(f"{RAW}/Raw Data (IMC)/NYP Raw Google Campaign report.xlsx", 0)
header = rows[2]; h = hdr_index(header)
for row in rows[3:]:
    if not any(row): continue
    add('Google Ads', g(row,'Campaign'), impressions=g(row,'Impr.'), clicks=g(row,'Clicks'),
        conversions=g(row,'Conversions'), spend=g(row,'Cost'))

# 6) YouTube xlsx (sheet 0 = YouTube Ad, header row 1 -> index 0)
rows = xlsx_rows(f"{RAW}/Campaign/Raw Data (GroupM)/YouTube Raw Data_2025 09 09 .xlsx", 0)
header = rows[0]; h = hdr_index(header)
for row in rows[1:]:
    if not any(row): continue
    add('YouTube', g(row,'Line Item'), impressions=g(row,'Impressions'), clicks=g(row,'Clicks'),
        video_views=g(row,'TrueView: Views'), spend=g(row,'Spends'))

# write output
cols = ['Platform','Campaign','Marketing Objective','Impressions','Reach','Clicks','Link Clicks','Video Views','Conversions','Spend','Start Date','End Date']
def r2(x): return round(x, 2)
with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(cols)
    for (plat, camp), r in sorted(acc.items()):
        w.writerow([r['Platform'], r['Campaign'], r['Objective'],
                    int(round(r['Impressions'])), int(round(r['Reach'])), int(round(r['Clicks'])),
                    int(round(r['LinkClicks'])), int(round(r['VideoViews'])), r2(r['Conversions']),
                    r2(r['Spend']), r['Start'], r['End']])
print("rows:", len(acc))

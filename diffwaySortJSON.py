import os
import json
import glob
import shutil
from datetime import datetime, time
from dateutil import parser
import pandas as pd

###############################################################################
# CONFIG / SCHEDULES
###############################################################################

SIM_MANNEQUINS = {
    "Sim1": ["Dave","Chuck"],
    "Sim2": ["Freddy","Oscar"],
    "Sim3": ["Dave","Chuck"],
    "Sim4": ["Dave","Chuck"],
    "Sim5": ["Freddy","Oscar","Matt"]
}

MANNEQUIN_MAP = {
    "AI23F013939": "Dave",
    "AI23H014090": "Chuck",
    "AI15F004305": "Freddy",
    "AI15D003889": "Matt",
    "AI20C009617": "Oscar"
}

def t(hhmm):
    """Utility to parse e.g. 925 => time(9,25)."""
    s = str(hhmm)
    if len(s)<=2:
        return time(int(s),0)
    hh = int(s[:-2])
    mm = int(s[-2:])
    return time(hh, mm)

SIM_SCHEDULES = {
    "Sim1": [(t(830),  t(955)),
             (t(955),  t(1120)),
             (t(1120), t(1245)),
             (t(1305), t(1430)),
             (t(1430), t(1555)),
             (t(1555), t(1720))],
    "Sim2": [(t(800),  t(920)),
             (t(920),  t(1040)),
             (t(1040), t(1200)),
             (t(1220), t(1340)),
             (t(1340), t(1500)),
             (t(1500), t(1620))],
    "Sim3": [(t(800),  t(930)),
             (t(930),  t(1100)),
             (t(1100), t(1230)),
             (t(1250), t(1420)),
             (t(1420), t(1550)),
             (t(1550), t(1720))],
    "Sim4": [(t(800),  t(925)),
             (t(925),  t(1050)),
             (t(1050), t(1215)),
             (t(1235), t(1400)),
             (t(1400), t(1525)),
             (t(1525), t(1650))],
    "Sim5": [(t(800),  t(910)),
             (t(910),  t(1020)),
             (t(1020), t(1130)),
             (t(1150), t(1300)),
             (t(1300), t(1410)),
             (t(1410), t(1520))]
}

COURSE_DATE_RANGES = [
    ("10/14","10/18","2025A"),
    ("10/28","11/01","2025B"),
    ("11/18","11/22","2025C"),
    ("12/09","12/13","2025D"),
    ("01/13","01/17","2025E"),
    ("01/27","01/31","2025F"),
    ("02/17","02/21","2025G/H"),
    ("02/24","02/28","2025H"),
    ("03/24","03/28","2025I"),
    ("04/14","04/18","2025J"),
    ("05/05","05/09","2025K/L"),
    ("05/12","05/16","2025L"),
    ("06/09","06/13","2025M"),
    ("06/23","06/27","2025N"),
]

COURSE_START_DATES = {
    "2025A":"2024-10-14",
    "2025B":"2024-10-28",
    "2025C":"2024-11-18",
    "2025D":"2024-12-09",
    "2025E":"2025-01-13",
    "2025F":"2025-01-27",
    "2025G/H":"2025-02-17",
    "2025H":"2025-02-24",
    "2025I":"2025-03-24",
    "2025J":"2025-04-14",
    "2025K/L":"2025-05-05",
    "2025L":"2025-05-12",
    "2025M":"2025-06-09",
    "2025N":"2025-06-23"
}

DAY_OFFSET_TO_SIM = {
    0:"Sim1",
    1:"Sim2",
    2:"Sim3",
    3:"Sim4",
    4:"Sim5"
}

###############################################################################
# HELPER: find course from date
###############################################################################
def parse_mmdd(s):
    m,d = s.split("/")
    return int(m), int(d)

def get_course_for_date(dt_obj):
    fm, fd = dt_obj.month, dt_obj.day
    for (start_s, end_s, cname) in COURSE_DATE_RANGES:
        sm, sd = parse_mmdd(start_s)
        em, ed = parse_mmdd(end_s)
        ok_start = (fm>sm) or (fm==sm and fd>=sd)
        ok_end   = (fm<em) or (fm==em and fd<=ed)
        if ok_start and ok_end:
            return cname
    return None

def get_sim_for_course_date(course, dt_obj):
    """Compute day offset from course start => pick Sim1..Sim5 (Mon-Fri)."""
    if not course or course not in COURSE_START_DATES:
        return None
    try:
        cstart = datetime.strptime(COURSE_START_DATES[course], "%Y-%m-%d")
    except:
        return None
    diff = (dt_obj.date() - cstart.date()).days
    return DAY_OFFSET_TO_SIM.get(diff)

def in_sim_time_window(dt_obj, sim):
    """Check if dt_obj.time() is within the known schedule windows for that sim."""
    if sim not in SIM_SCHEDULES: 
        return False
    the_time = dt_obj.time()
    for (startT, endT) in SIM_SCHEDULES[sim]:
        if startT <= the_time <= endT:
            return True
    return False

###############################################################################
# PARSE JSON => ROWS
###############################################################################
def get_trend_val(trObj):
    """Return #text if not unmonitored/invalid, else None."""
    if not trObj: return None
    ds = trObj.get("DataState")
    st = trObj.get("DataStatus")
    if ds in ("unmonitored","invalid"):
        return None
    if st==1:
        return None
    return trObj.get("Val",{}).get("#text")

def parse_trend_rpt(tr, devS):
    """Return list of row dict from a single TrendRpt block."""
    out = []
    dt_s = tr.get("StdHdr",{}).get("DevDateTime")
    try:
        dt_o = parser.parse(dt_s)
    except:
        dt_o = None

    trend = tr.get("Trend",{})
    row = {}
    row["TimeObj"]  = dt_o
    row["TimeStr"]  = dt_s
    row["DevSerial"]= devS

    # temps
    tmpA = trend.get("Temp", [])
    for i, tA in enumerate(tmpA, start=1):
        row[f"Temp{i}"] = get_trend_val(tA.get("TrendData"))

    # HR
    hrO = trend.get("Hr",{})
    row["Hr"] = get_trend_val(hrO.get("TrendData"))

    # FiCO2
    fiO = trend.get("Fico2",{})
    row["FiCO2"] = get_trend_val(fiO.get("TrendData"))

    # SpO2 block
    sO2 = trend.get("Spo2",{})
    row["SpO2"]  = get_trend_val(sO2.get("TrendData"))
    row["SpMet"] = get_trend_val(sO2.get("SpMet",{}).get("TrendData"))
    row["SpCo"]  = get_trend_val(sO2.get("SpCo",{}).get("TrendData"))
    row["PVI"]   = get_trend_val(sO2.get("PVI",{}).get("TrendData"))
    row["PI"]    = get_trend_val(sO2.get("PI",{}).get("TrendData"))
    row["SpOC"]  = get_trend_val(sO2.get("SpOC",{}).get("TrendData"))
    row["SpHb"]  = get_trend_val(sO2.get("SpHb",{}).get("TrendData"))

    # NIBP
    nA = trend.get("Nibp",{})
    row["NIBP_SYS"] = get_trend_val(nA.get("Sys",{}).get("TrendData"))
    row["NIBP_DIA"] = get_trend_val(nA.get("Dia",{}).get("TrendData"))
    row["NIBP_MAP"] = get_trend_val(nA.get("Map",{}).get("TrendData"))

    # IBP
    ibp_list = trend.get("Ibp", [])
    for ibI in ibp_list:
        cN = ibI.get("@ChanNum")
        row[f"IBP{cN}_SYS"] = get_trend_val(ibI.get("Sys",{}).get("TrendData"))
        row[f"IBP{cN}_DIA"] = get_trend_val(ibI.get("Dia",{}).get("TrendData"))
        row[f"IBP{cN}_MAP"] = get_trend_val(ibI.get("Map",{}).get("TrendData"))

    # EtCO2
    eC = trend.get("Etco2",{})
    row["EtCO2"] = get_trend_val(eC.get("TrendData"))

    # Resp
    rR = trend.get("Resp",{})
    row["RespRate"] = get_trend_val(rR.get("TrendData"))

    out.append(row)
    return out

def parse_one_json(json_path):
    """Flatten all TrendRpt in a single JSON => list of rows."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        recs = data["ZOLL"]["FullDisclosure"][0]["FullDisclosureRecord"]
    except:
        return []

    # find device serial
    devS = None
    for rr in recs:
        if "DeviceConfiguration" in rr:
            devS = rr["DeviceConfiguration"].get("DeviceSerialNumber")
            break

    out = []
    for rr in recs:
        if "TrendRpt" in rr:
            out += parse_trend_rpt(rr["TrendRpt"], devS)

    return out

###############################################################################
# MAIN
###############################################################################
def main():
    input_folder = "/Users/rajveersingh/Downloads/propaq_data_testing/"
    output_folder= "/Users/rajveersingh/Downloads/sorted_data_testing/"
    os.makedirs(output_folder, exist_ok=True)

    # 1) Flatten all JSON => big DataFrame
    json_files = glob.glob(os.path.join(input_folder,"*.json"))
    big_rows = []
    for jf in json_files:
        base = os.path.basename(jf)
        R = parse_one_json(jf)
        for r in R:
            r["SourceFile"] = base
        big_rows.extend(R)

    df = pd.DataFrame(big_rows)
    print(f"[INFO] Flattened {len(df)} rows from {len(json_files)} JSON files.")
    # drop rows with no TimeObj
    if "TimeObj" in df.columns:
        df.dropna(subset=["TimeObj"], inplace=True)
        df.sort_values("TimeObj", inplace=True)
        df.reset_index(drop=True, inplace=True)
    else:
        print("[WARN] No TimeObj column found. Possibly no data.")
        return

    # 2) rawMannequin from DevSerial
    def rawman(ds):
        return MANNEQUIN_MAP.get(ds, None)
    df["rawMannequin"] = df["DevSerial"].apply(rawman)

    # 3) find course, sim
    df["Course"] = df["TimeObj"].apply(get_course_for_date)

    def pick_sim(row):
        c_ = row["Course"]
        t_ = row["TimeObj"]
        return get_sim_for_course_date(c_, t_) if c_ else None
    df["Sim"] = df.apply(pick_sim, axis=1)

    # 4) check if in sim schedule window
    def is_in_window(row):
        s_ = row["Sim"]
        dt_= row["TimeObj"]
        if not s_: return False
        return in_sim_time_window(dt_, s_)
    df["InSimWindow"] = df.apply(is_in_window, axis=1)

    # 5) overrideMannequin = rawMannequin initially
    df["overrideMannequin"] = df["rawMannequin"]

    # help grouping
    df["DateStr"] = df["TimeObj"].dt.strftime("%Y-%m-%d")

    # We'll define a function that tries to fix the group if there's a mismatch
    def correct_set(sim):
        return set(SIM_MANNEQUINS.get(sim, []))

    def attempt_override(subdf):
        # only fix rows that are in the window
        fixmask = subdf["InSimWindow"]==True
        fixable = subdf[ fixmask ].copy()
        s_ = subdf["Sim"].iloc[0]
        cset = correct_set(s_)
        if not cset:
            return subdf
        # find which mannequins are actually used
        used = set(x for x in fixable["rawMannequin"].unique() if x)
        # find missing = cset - used
        missing = list(cset - used)
        if not missing:
            # no missing => maybe everything is correct
            return subdf

        # find "invalid" = rows where rawMannequin not in cset
        invalid_mask = ~fixable["rawMannequin"].isin(cset) & fixable["rawMannequin"].notna()
        invalid_idx  = fixable[invalid_mask].index

        # naive approach: for each invalid row, if there's still a missing item, override it
        # e.g. if missing = ["Oscar"], we override the device to "Oscar"
        missingQ = missing[:]
        for ridx in invalid_idx:
            if missingQ:
                newM = missingQ.pop(0)
                fixable.at[ridx,"overrideMannequin"] = newM

        # put it back
        newsub = pd.concat([ fixable, subdf[~fixmask] ], ignore_index=True)
        newsub.sort_values("TimeObj", inplace=True)
        return newsub

    # group by (Course,Sim,DateStr) => fix each group
    fixed_list = []
    for (co,si,ds), subset in df.groupby(["Course","Sim","DateStr"]):
        local = attempt_override(subset)
        fixed_list.append(local)

    finalDF = pd.concat(fixed_list, ignore_index=True)
    finalDF.sort_values("TimeObj", inplace=True)

    # 6) define IsValid
    def is_valid(row):
        if pd.isnull(row["Course"]): return False
        if pd.isnull(row["Sim"]): return False
        if row["InSimWindow"]!=True: return False
        s_ = row["Sim"]
        ov = row["overrideMannequin"]
        if not ov: return False
        return ov in SIM_MANNEQUINS.get(s_,[])
    finalDF["IsValid"] = finalDF.apply(is_valid, axis=1)

    # separate
    validDF   = finalDF[ finalDF["IsValid"]==True ].copy()
    unknownDF = finalDF[ finalDF["IsValid"]==False].copy()

    # optional: write unknown to CSV
    if not unknownDF.empty:
        un_path = os.path.join(output_folder,"unknown_rows.csv")
        unknownDF.to_csv(un_path, index=False)
        print(f"[INFO] wrote unknown => {un_path}")

    # group & output valid
    print(f"[INFO] valid rows = {len(validDF)}")
    if validDF.empty:
        return

    # build folder structure <Course>/<Sim>/<overrideMannequin>/<YYYY-MM-DD> ...
    validDF["DateStr"] = validDF["TimeObj"].dt.strftime("%Y-%m-%d")
    for (co, si, man, ds) in validDF.groupby(["Course","Sim","overrideMannequin","DateStr"]).groups.keys():
        sub = validDF[(validDF["Course"]==co)&(validDF["Sim"]==si)&
                      (validDF["overrideMannequin"]==man)&(validDF["DateStr"]==ds)].copy()
        sub.sort_values("TimeObj", inplace=True)
        sub.reset_index(drop=True, inplace=True)
        folder = os.path.join(output_folder, co.replace("/","_"), si, man, ds)
        os.makedirs(folder, exist_ok=True)
        xname = f"{co}_{si}_{man}_{ds.replace('-','')}.xlsx".replace("/","_")
        xp = os.path.join(folder, xname)
        sub.to_excel(xp, index=False)
        print(f"[WRITE] => {xp} : {len(sub)} rows")

if __name__=="__main__":
    main()

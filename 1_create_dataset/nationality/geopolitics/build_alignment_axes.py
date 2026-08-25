# -*- coding: utf-8 -*-
"""
Two-axis geopolitical alignment index: US axis and China axis, one score per country.

    axis_P(c) = engagement_P(c) - hostility_P(c)          in [-1, +1],  P in {US, CN}

engagement_P in [0,1] is an equal-weight mean of three measured layers:
    1/3   UNGA voting agreement with P     (Bailey/Strezhnev/Voeten dyadic agreement,
                                            sessions 2022-2024, min-max rescaled)
    1/3   security ties with P             (hand-coded treaty/quasi-alliance tier;
                                            SIPRI TIV share of arms imports 2020-2025;
                                            for the US axis also US troops in country)
    1/3   trade dependence on P            ((X+M with P)/(X+M with world), IMF DOTS
                                            2022-2024, capped at 50% = full dependence)
The published sample keeps only countries with all three layers available for both poles.

hostility_P in [0,1] is the max over documented conflict markers (war, comprehensive
sanctions, militarized dispute, coercion). Max, not sum, to avoid double counting.

Sources (downloaded 2026-08-25):
  - UNGA:  Voeten dataverse doi:10.7910/DVN/LEJUQZ, July-2025 release (through session 79 / 2024)
  - Arms:  SIPRI Arms Transfers Database (armstransfers.sipri.org), deliveries 2020-2025, TIV
  - Trade: IMF Direction of Trade Statistics via DBnomics mirror (through 2024)
  - Troops: Flynn et al. troopdata rebuild (github.com/meflynn/troopdata), 2022-2024 active duty
  - Hand-coded tables below: each entry carries its documentary basis, as of Aug 2026.

Run:  python build_alignment_axes.py     (writes alignment_axes.csv + alignment_scatter.png)
"""
import os, re, io
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# --------------------------------------------------------------------------------------
# 0. Country identity: ISO3 is the canonical key
# --------------------------------------------------------------------------------------
ip = pd.read_csv(os.path.join(RAW, "idealpoints_1946_2024.csv"))
ip["iso3c"] = ip.iso3c.replace({"YUG": "SRB"})       # COW keeps Serbia under Yugoslavia's code
ip24 = ip[ip.year == 2024].dropna(subset=["iso3c"]).copy()
# UN members with votes since 2021 (Venezuela lost its UNGA vote in 2022, Art. 19 arrears)
UNIVERSE = set(ip[ip.year >= 2021].dropna(subset=["iso3c"]).iso3c) | {"TWN", "XKX"}
CCODE2ISO = ip.dropna(subset=["iso3c"]).drop_duplicates("ccode", keep="last").set_index("ccode").iso3c.to_dict()
NAME2ISO = {}
for _, r in ip.dropna(subset=["iso3c"]).drop_duplicates("countryname", keep="last").iterrows():
    NAME2ISO[r.countryname.strip().lower()] = r.iso3c

def _norm(s):
    s = s.strip().lower()
    s = re.sub(r"[’'`’]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

# SIPRI / DOTS naming quirks -> ISO3
NAME_FIX = {
    "united states": "USA", "russia": "RUS", "china": "CHN", "south korea": "KOR",
    "north korea": "PRK", "viet nam": "VNM", "vietnam": "VNM", "syria": "SYR",
    "iran": "IRN", "laos": "LAO", "bolivia": "BOL", "venezuela": "VEN", "tanzania": "TZA",
    "moldova": "MDA", "cote divoire": "CIV", "ivory coast": "CIV", "dr congo": "COD",
    "congo, dr": "COD", "democratic republic of the congo": "COD", "congo": "COG",
    "republic of the congo": "COG", "cape verde": "CPV", "cabo verde": "CPV",
    "bosnia-herzegovina": "BIH", "bosnia and herzegovina": "BIH", "brunei": "BRN",
    "brunei darussalam": "BRN", "czechia": "CZE", "czech republic": "CZE",
    "timor-leste": "TLS", "east timor": "TLS", "north macedonia": "MKD",
    "macedonia (fyrom)": "MKD", "micronesia": "FSM", "myanmar": "MMR", "burma": "MMR",
    "taiwan": "TWN", "trinidad and tobago": "TTO", "trinidad & tobago": "TTO",
    "turkey": "TUR", "turkiye": "TUR", "uae": "ARE", "united arab emirates": "ARE",
    "united kingdom": "GBR", "uk": "GBR", "kosovo": "XKX", "palestine": "PSE",
    "gambia": "GMB", "the gambia": "GMB", "bahamas": "BHS", "the bahamas": "BHS",
    "eswatini": "SWZ", "swaziland": "SWZ", "st kitts and nevis": "KNA",
    "saint kitts and nevis": "KNA", "st lucia": "LCA", "saint lucia": "LCA",
    "st vincent and the grenadines": "VCT", "saint vincent and the grenadines": "VCT",
    "sao tome and principe": "STP", "guinea-bissau": "GNB", "equatorial guinea": "GNQ",
    "central african republic": "CAF", "south sudan": "SSD", "sri lanka": "LKA",
    "papua new guinea": "PNG", "solomon islands": "SLB", "marshall islands": "MHL",
    "dominican republic": "DOM", "el salvador": "SLV", "burkina faso": "BFA",
    "sierra leone": "SLE", "saudi arabia": "SAU", "south africa": "ZAF",
    "new zealand": "NZL", "netherlands": "NLD", "the netherlands": "NLD",
    "russian federation": "RUS", "republic of korea": "KOR", "korea, south": "KOR",
    "korea, north": "PRK", "cambodia": "KHM", "libya": "LBY",
    "serbia": "SRB", "antigua and barbuda": "ATG",
}

def to_iso3(name):
    n = _norm(name)
    if n in NAME_FIX:
        return NAME_FIX[n]
    return NAME2ISO.get(n)

ISO2TO3 = {
 'AF':'AFG','AL':'ALB','DZ':'DZA','AD':'AND','AO':'AGO','AG':'ATG','AR':'ARG','AM':'ARM',
 'AU':'AUS','AT':'AUT','AZ':'AZE','BS':'BHS','BH':'BHR','BD':'BGD','BB':'BRB','BY':'BLR',
 'BE':'BEL','BZ':'BLZ','BJ':'BEN','BT':'BTN','BO':'BOL','BA':'BIH','BW':'BWA','BR':'BRA',
 'BN':'BRN','BG':'BGR','BF':'BFA','BI':'BDI','CV':'CPV','KH':'KHM','CM':'CMR','CA':'CAN',
 'CF':'CAF','TD':'TCD','CL':'CHL','CN':'CHN','CO':'COL','KM':'COM','CD':'COD','CG':'COG',
 'CR':'CRI','CI':'CIV','HR':'HRV','CU':'CUB','CY':'CYP','CZ':'CZE','DK':'DNK','DJ':'DJI',
 'DM':'DMA','DO':'DOM','EC':'ECU','EG':'EGY','SV':'SLV','GQ':'GNQ','ER':'ERI','EE':'EST',
 'SZ':'SWZ','ET':'ETH','FJ':'FJI','FI':'FIN','FR':'FRA','GA':'GAB','GM':'GMB','GE':'GEO',
 'DE':'DEU','GH':'GHA','GR':'GRC','GD':'GRD','GT':'GTM','GN':'GIN','GW':'GNB','GY':'GUY',
 'HT':'HTI','HN':'HND','HK':'HKG','HU':'HUN','IS':'ISL','IN':'IND','ID':'IDN','IR':'IRN',
 'IQ':'IRQ','IE':'IRL','IL':'ISR','IT':'ITA','JM':'JAM','JP':'JPN','JO':'JOR','KZ':'KAZ',
 'KE':'KEN','KI':'KIR','KP':'PRK','KR':'KOR','KW':'KWT','KG':'KGZ','LA':'LAO','LV':'LVA',
 'LB':'LBN','LS':'LSO','LR':'LBR','LY':'LBY','LT':'LTU','LU':'LUX','MO':'MAC','MG':'MDG',
 'MW':'MWI','MY':'MYS','MV':'MDV','ML':'MLI','MT':'MLT','MH':'MHL','MR':'MRT','MU':'MUS',
 'MX':'MEX','FM':'FSM','MD':'MDA','MC':'MCO','MN':'MNG','ME':'MNE','MA':'MAR','MZ':'MOZ',
 'MM':'MMR','NA':'NAM','NR':'NRU','NP':'NPL','NL':'NLD','NZ':'NZL','NI':'NIC','NE':'NER',
 'NG':'NGA','MK':'MKD','NO':'NOR','OM':'OMN','PK':'PAK','PW':'PLW','PA':'PAN','PG':'PNG',
 'PY':'PRY','PE':'PER','PH':'PHL','PL':'POL','PT':'PRT','QA':'QAT','RO':'ROU','RU':'RUS',
 'RW':'RWA','WS':'WSM','SM':'SMR','ST':'STP','SA':'SAU','SN':'SEN','RS':'SRB','SC':'SYC',
 'SL':'SLE','SG':'SGP','SK':'SVK','SI':'SVN','SB':'SLB','SO':'SOM','ZA':'ZAF','SS':'SSD',
 'ES':'ESP','LK':'LKA','KN':'KNA','LC':'LCA','VC':'VCT','SD':'SDN','SR':'SUR','SE':'SWE',
 'CH':'CHE','SY':'SYR','TW':'TWN','TJ':'TJK','TZ':'TZA','TH':'THA','TL':'TLS','TG':'TGO',
 'TO':'TON','TT':'TTO','TN':'TUN','TR':'TUR','TM':'TKM','TV':'TUV','UG':'UGA','UA':'UKR',
 'AE':'ARE','GB':'GBR','US':'USA','UY':'URY','UZ':'UZB','VU':'VUT','VE':'VEN','VN':'VNM',
 'YE':'YEM','ZM':'ZMB','ZW':'ZWE','XK':'XKX','KV':'XKX','AW':'ABW','CW':'CUW',
}

# --------------------------------------------------------------------------------------
# 1. UNGA voting agreement with each pole (sessions 77-79 = calendar 2022-2024)
# --------------------------------------------------------------------------------------
ag = pd.read_csv(os.path.join(RAW, "agreement_us_cn_2015plus.csv"))
ag = ag[ag.year.between(2022, 2024)]

def pole_agreement(pole_ccode):
    a = ag[(ag.ccode1 == pole_ccode) | (ag.ccode2 == pole_ccode)].copy()
    a["other"] = np.where(a.ccode1 == pole_ccode, a.ccode2, a.ccode1)
    m = a.groupby("other").agree.mean()
    m.index = m.index.map(CCODE2ISO)
    return m.dropna()

unga_us_raw = pole_agreement(2)      # COW ccode 2  = USA
unga_cn_raw = pole_agreement(710)    # COW ccode 710 = China

def minmax(s):
    return (s - s.min()) / (s.max() - s.min())

unga_us = minmax(unga_us_raw)
unga_cn = minmax(unga_cn_raw)

# Ideal-point check column (Voeten's single latent dimension, 2024)
ipt = ip24.set_index("iso3c").idealpointfp
ideal_reldist = (ipt - ipt["USA"]).abs() - (ipt - ipt["CHN"]).abs()   # >0 = closer to China

# --------------------------------------------------------------------------------------
# 2. SIPRI arms-import shares 2020-2025 (TIV)
# --------------------------------------------------------------------------------------
def read_sipri(fname):
    txt = open(os.path.join(RAW, fname), encoding="utf8").read()
    lines = txt.splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("Recipient,"))
    body = [l for l in lines[start:] if l.strip()]
    df = pd.read_csv(io.StringIO("\n".join(body)))
    total_col = next(c for c in df.columns if re.match(r"^\d{4}-\d{4}$", c))
    df = df[["Recipient", total_col]].rename(columns={total_col: "tiv"})
    df = df[~df.Recipient.str.contains(r"\*|Total", na=False)]
    df["iso3"] = df.Recipient.map(to_iso3)
    unmatched = df[df.iso3.isna()].Recipient.tolist()
    if unmatched:
        print(f"  [sipri:{fname}] sin mapear (se descartan): {unmatched}")
    return df.dropna(subset=["iso3"]).set_index("iso3").tiv

arms_total = read_sipri("sipri_importexport_2020_2025.csv")
arms_us = read_sipri("sipri_from_USA_2020_2025.csv")
arms_cn = read_sipri("sipri_from_CHI_2020_2025.csv")
arms_ru = read_sipri("sipri_from_RUS_2020_2025.csv")

MIN_TIV = 50  # <50M TIV over 6y: import volume too small to signal orientation -> missing
def arms_share(from_pole):
    sh = (from_pole.reindex(arms_total.index).fillna(0) / arms_total).clip(0, 1)
    return sh[arms_total >= MIN_TIV]

arms_share_us = arms_share(arms_us)
arms_share_cn = arms_share(arms_cn)
arms_share_ru = arms_share(arms_ru)

# --------------------------------------------------------------------------------------
# 3. Trade dependence (IMF DOTS 2022-2024): (X+M with pole) / (X+M with world)
# --------------------------------------------------------------------------------------
dt = pd.read_csv(os.path.join(RAW, "dots_trade.csv"))
dt = dt[dt.year.between(2022, 2024)]
dt["iso3"] = dt.ref_area.map(ISO2TO3)
dt = dt.dropna(subset=["iso3"])
piv = dt.pivot_table(index=["iso3", "year"], columns=["counterpart", "indicator"],
                     values="value", aggfunc="sum")

def trade_share(pole):
    x = piv.get((pole, "TXG_FOB_USD"), pd.Series(dtype=float))
    m = piv.get((pole, "TMG_CIF_USD"), pd.Series(dtype=float))
    xw = piv.get(("W00", "TXG_FOB_USD"), pd.Series(dtype=float))
    mw = piv.get(("W00", "TMG_CIF_USD"), pd.Series(dtype=float))
    tot = xw.add(mw, fill_value=0)
    with_p = x.reindex(tot.index).fillna(0).add(m.reindex(tot.index).fillna(0), fill_value=0)
    sh = (with_p / tot).groupby("iso3").mean().clip(0, 1)
    return (sh / 0.50).clip(0, 1)      # 50% of total trade with the pole = full dependence

trade_us = trade_share("US")
trade_cn = trade_share("CN")

# --------------------------------------------------------------------------------------
# 4. US troops stationed (2022-2024 mean, log scale)
# --------------------------------------------------------------------------------------
tr = pd.read_csv(os.path.join(RAW, "us_troops_2022_2024.csv"))
troops = tr.groupby("iso3c").troops_ad.mean()
troops = troops[troops >= 100]                       # below ~100 = embassy detachments
troops_us = np.log10(troops) / np.log10(troops.max())  # 100 -> ~0.4, 55k (JPN) -> 1.0
troops_us = troops_us.clip(0, 1)

# --------------------------------------------------------------------------------------
# 5. Hand-coded layer A: treaty / quasi-alliance tier (0-1), documented basis per entry
# --------------------------------------------------------------------------------------
NATO = ["ALB","BEL","BGR","CAN","HRV","CZE","DNK","EST","FIN","FRA","DEU","GRC","HUN",
        "ISL","ITA","LVA","LTU","LUX","MNE","NLD","MKD","NOR","POL","PRT","ROU","SVK",
        "SVN","ESP","SWE","TUR","GBR"]
RIO = ["ARG","BHS","BRA","CHL","COL","CRI","DOM","SLV","GTM","HTI","HND","PAN","PRY",
       "PER","TTO","URY"]                            # Rio Pact: weak hemispheric treaty

US_ALLY = {c: 1.0 for c in NATO}                     # North Atlantic Treaty art. 5
US_ALLY.update({c: 0.5 for c in RIO})
US_ALLY.update({
    "JPN": 1.0,   # 1960 Treaty of Mutual Cooperation and Security
    "KOR": 1.0,   # 1953 Mutual Defense Treaty
    "PHL": 1.0,   # 1951 Mutual Defense Treaty
    "AUS": 1.0,   # ANZUS 1951
    "THA": 1.0,   # Manila Pact 1954 + Thanat-Rusk 1962 (formal, if drifting)
    "NZL": 0.7,   # ANZUS partially suspended for NZ since 1986
    "FSM": 1.0, "MHL": 1.0, "PLW": 1.0,   # Compacts of Free Association: US runs defense
    "TWN": 0.8,   # Taiwan Relations Act commitment, arms; no formal treaty
    "ISR": 0.8,   # MNNA+, QME statute, 2026 co-belligerent vs Iran
    "EGY": 0.5, "JOR": 0.5, "KWT": 0.5, "MAR": 0.5, "PAK": 0.5, "TUN": 0.5,
    "BHR": 0.5, "KEN": 0.5,               # Major Non-NATO Allies
    "QAT": 0.6,   # MNNA + Sept 2025 US executive-order security guarantee
    "UKR": 0.55,  # 2024 10-year bilateral security agreement + wartime patron
    "SAU": 0.35,  # de facto security patron, no treaty (2025 defense-pact talks)
    "ARE": 0.4,   # Major Defense Partner designation 2024
    "SGP": 0.35,  # Major Security Cooperation Partner, MDCA basing
    "COL": 0.55,  # MNNA 2022 + NATO global partner (overrides Rio 0.5)
    "IND": 0.3,   # Major Defense Partner, Quad, COMCASA/BECA
    "GEO": 0.2,   # aspirant partner
    "VNM": 0.1,   # US-Vietnam CSP 2023 (political, not military)
    "XKX": 0.6,   # de facto protectorate: KFOR/Camp Bondsteel, security fully US-dependent
})

CN_ALLY = {
    "PRK": 1.0,   # 1961 Treaty of Friendship, Co-operation and Mutual Assistance (only defense treaty)
    "RUS": 0.7,   # "no-limits" partnership, joint exercises/patrols, no treaty
    "PAK": 0.65,  # all-weather strategic cooperative partnership, JF-17 co-production, CPEC
    "BLR": 0.55,  # all-weather partnership 2023 + SCO accession 2024
    "KHM": 0.5,   # Ream naval base access, Golden Dragon exercises
    "IRN": 0.45,  # 25-year strategic agreement 2021 + SCO member 2023
    "SRB": 0.45,  # CSP + "shared future" 2024 + HQ-22/FK-3 arms purchases
    "MMR": 0.4, "LAO": 0.4,               # corridor states, "shared future", arms/deps
    "CUB": 0.4,   # strategic partnership, reported signals facilities
    "DJI": 0.35,  # PLA support base 2017
    "NIC": 0.35,  # strategic partnership 2023, BRI
    "SLB": 0.35,  # 2022 bilateral security agreement
    "KAZ": 0.35, "KGZ": 0.35, "TJK": 0.35, "UZB": 0.35,  # SCO + permanent CSPs (UZB all-weather 2024)
    "AZE": 0.3,   # CSP 2024, upgraded 2025
    "HUN": 0.3,   # all-weather CSP May 2024 (inside NATO)
    "ETH": 0.3,   # all-weather CSP 2023
    "ZWE": 0.3, "DZA": 0.3,               # long CSPs with military component
    "IND": 0.3,   # SCO full member (border dispute lives in hostility)
    "VNM": 0.3,   # "community of shared future" 2023 (disputes live in hostility)
    "TKM": 0.25, "EGY": 0.25, "ARE": 0.25, "THA": 0.25, "LKA": 0.25, "TZA": 0.25,
    "GNQ": 0.25, "ERI": 0.25, "VEN": 0.25,  # VEN: was 0.45 under Maduro; post-Jan-2026 flux
    "SAU": 0.2, "IDN": 0.2, "BGD": 0.2, "MNG": 0.2, "ZAF": 0.2, "BOL": 0.2,
    "PER": 0.2,   # CSP + Chancay megaport (COSCO) 2024
    "SDN": 0.2, "MLI": 0.2, "BFA": 0.2, "NER": 0.2, "AFG": 0.2,
    "BRA": 0.15, "NGA": 0.15, "KEN": 0.15,
    "ARG": 0.1, "CHL": 0.1,               # ARG: CSP 2014 frozen under Milei
}

# --------------------------------------------------------------------------------------
# 6. Hand-coded layer B: hostility markers (0-1), max is taken; documented basis
# --------------------------------------------------------------------------------------
US_HOSTILITY = {
    "IRN": 1.0,   # at war with US/Israel since Feb 2026; naval blockade Aug 2026
    "RUS": 0.85,  # extensive sanctions; arming Ukraine against it
    "PRK": 0.85,  # comprehensive sanctions, formal enmity
    "CUB": 0.7,   # comprehensive embargo, state sponsor list
    "VEN": 0.55,  # Jan 2026 US raid (Maduro capture); sanctions legacy; US-imposed transition
    "AFG": 0.5,   # Taliban government unrecognized, sanctions
    "BLR": 0.5,   # sanctions, co-belligerent staging for Russia
    "NIC": 0.4,   # sanctions, adversarial
    "MMR": 0.35,  # junta sanctions
    "SDN": 0.3, "MLI": 0.3, "BFA": 0.3, "NER": 0.3,  # juntas expelled US forces / Wagner ties
    "ERI": 0.25, "ZWE": 0.25,             # standing sanctions programs
    "SYR": 0.2,   # residual sanctions; post-Assad relief since 2025 (UNGA leg is still Assad-era votes)
    "CHN": 0.6,   # the rivalry itself: tech/tariff war, Taiwan deterrence
}

CN_HOSTILITY = {
    "TWN": 1.0,   # claimed territory, explicit threat of force, daily PLA pressure
    "PHL": 0.6,   # active South China Sea clashes (rammings, water cannons)
    "JPN": 0.5,   # Senkaku + Nov 2025 Takaichi crisis (coercive measures, threats)
    "IND": 0.45,  # militarized LAC border (Galwan 2020; partial 2024-25 thaw)
    "VNM": 0.35,  # South China Sea standoffs despite party ties
    "LTU": 0.3,   # 2021-24 trade blockade over Taiwan office (partly normalized)
    "USA": 0.6,   # the rivalry itself
    "CAN": 0.2,   # hostage diplomacy legacy, election interference, 2024-25 tariffs
    "NLD": 0.2,   # ASML export-control fight, 2025 Nexperia escalation
    "CZE": 0.15, "MYS": 0.15,             # Taiwan friction / Luconia standoffs
    "AUS": 0.15,  # 2020-22 trade coercion, since eased
    "KOR": 0.1, "GBR": 0.1, "IDN": 0.1,   # THAAD legacy / spy rows / Natuna incursions
}

# --------------------------------------------------------------------------------------
# 7. Compose the two axes
# --------------------------------------------------------------------------------------
W_UNGA = W_SEC = W_TRADE = 1 / 3

rows = []
for iso in sorted(UNIVERSE):
    r = {"iso3": iso}
    r["unga_us"] = unga_us.get(iso, np.nan);  r["unga_cn"] = unga_cn.get(iso, np.nan)
    r["unga_us_raw"] = unga_us_raw.get(iso, np.nan); r["unga_cn_raw"] = unga_cn_raw.get(iso, np.nan)
    r["arms_us"] = arms_share_us.get(iso, np.nan); r["arms_cn"] = arms_share_cn.get(iso, np.nan)
    r["arms_ru"] = arms_share_ru.get(iso, np.nan)
    r["trade_us"] = trade_us.get(iso, np.nan); r["trade_cn"] = trade_cn.get(iso, np.nan)
    r["troops_us"] = troops_us.get(iso, np.nan)
    r["ally_us"] = US_ALLY.get(iso, 0.0); r["ally_cn"] = CN_ALLY.get(iso, 0.0)
    r["host_us"] = US_HOSTILITY.get(iso, 0.0); r["host_cn"] = CN_HOSTILITY.get(iso, 0.0)
    r["ideal_reldist"] = ideal_reldist.get(iso, np.nan)

    # security sub-composite: US = alliance .5 / arms .3 / troops .2 ; CN = alliance .6 / arms .4
    def sub(parts):
        parts = [(w, v) for w, v in parts if not pd.isna(v)]
        if not parts: return np.nan
        tw = sum(w for w, _ in parts)
        return sum(w * v for w, v in parts) / tw
    sec_us = sub([(0.5, r["ally_us"]), (0.3, r["arms_us"]), (0.2, r["troops_us"])])
    sec_cn = sub([(0.6, r["ally_cn"]), (0.4, r["arms_cn"])])
    r["sec_us"], r["sec_cn"] = sec_us, sec_cn

    eng_us = sub([(W_UNGA, r["unga_us"]), (W_SEC, sec_us), (W_TRADE, r["trade_us"])])
    eng_cn = sub([(W_UNGA, r["unga_cn"]), (W_SEC, sec_cn), (W_TRADE, r["trade_cn"])])
    r["eng_us"], r["eng_cn"] = eng_us, eng_cn
    r["axis_us"] = (eng_us if not pd.isna(eng_us) else 0) - r["host_us"]
    r["axis_cn"] = (eng_cn if not pd.isna(eng_cn) else 0) - r["host_cn"]
    rows.append(r)

df = pd.DataFrame(rows).set_index("iso3")
# Canonical analysis sample: all three top-level layers observed for both poles.
# This deliberately excludes self-comparisons (USA/CHN), Taiwan, Kosovo, Venezuela,
# Andorra, Liechtenstein, Monaco, and Namibia.
complete_cols = ["unga_us", "sec_us", "trade_us", "unga_cn", "sec_cn", "trade_cn"]
df = df.dropna(subset=complete_cols).copy()
df["net_lean_us"] = df.axis_us - df.axis_cn

names = ip.dropna(subset=["iso3c"]).drop_duplicates("iso3c", keep="last").set_index("iso3c").countryname
names.loc["TWN"] = "Taiwan"; names.loc["XKX"] = "Kosovo"
PRETTY = {"DEU": "Germany", "SRB": "Serbia", "FSM": "Micronesia", "MMR": "Myanmar",
          "RUS": "Russia", "TZA": "Tanzania", "LAO": "Laos", "MDA": "Moldova",
          "BOL": "Bolivia", "VEN": "Venezuela", "IRN": "Iran", "SYR": "Syria",
          "PRK": "North Korea", "KOR": "South Korea", "VNM": "Vietnam", "CIV": "Ivory Coast",
          "STP": "Sao Tome and Principe"}
for k, v in PRETTY.items():
    names.loc[k] = v
df["name"] = names.reindex(df.index)

# quadrant classification against the median of the field (poles excluded)
field = df.drop(index=["USA", "CHN"], errors="ignore")
mx, my = field.axis_us.median(), field.axis_cn.median()
def quad(r):
    if r.axis_us < 0 and r.axis_cn < 0: return "rival de ambos"
    if r.axis_us < 0: return "rival de EEUU"
    if r.axis_cn < 0: return "rival de China"
    hi_us, hi_cn = r.axis_us >= mx, r.axis_cn >= my
    if hi_us and not hi_cn: return "pro-EEUU"
    if hi_cn and not hi_us: return "pro-China"
    if hi_us and hi_cn: return "doble juego (hedger)"
    return "no alineado (bajo con ambos)"
df["cuadrante"] = df.apply(quad, axis=1)

df = df.sort_values("net_lean_us", ascending=False)
out_cols = ["name", "axis_us", "axis_cn", "net_lean_us", "cuadrante",
            "eng_us", "eng_cn", "host_us", "host_cn",
            "unga_us", "unga_cn", "unga_us_raw", "unga_cn_raw",
            "sec_us", "sec_cn", "ally_us", "ally_cn",
            "arms_us", "arms_cn", "arms_ru", "troops_us",
            "trade_us", "trade_cn", "ideal_reldist"]
df[out_cols].round(4).to_csv(os.path.join(HERE, "alignment_axes.csv"), encoding="utf-8-sig")
print(f"\n{len(df)} países -> alignment_axes.csv | medianas: US {mx:.3f}, CN {my:.3f}")

# Strict groups used downstream. Weak leaners are intentionally omitted.
def strict_group(v):
    if v >= 0.45: return "aliado_eeuu_rival_china"
    if v < -0.45: return "aliado_china_rival_eeuu"
    if -0.15 <= v < 0.15: return "neutral_ambos"
    return None

groups = df.assign(grupo_estricto=df.net_lean_us.map(strict_group)).dropna(subset=["grupo_estricto"])
group_order = ["aliado_eeuu_rival_china", "aliado_china_rival_eeuu", "neutral_ambos"]
groups = groups.reset_index().sort_values(["grupo_estricto", "name"])
groups[["iso3", "name", "grupo_estricto", "axis_us", "axis_cn", "net_lean_us"]].round(4).to_csv(
    os.path.join(HERE, "alignment_groups_strict.csv"), index=False, encoding="utf-8-sig")

labels = {
    "aliado_eeuu_rival_china": "Aliados de EE.UU. y rivales de China",
    "aliado_china_rival_eeuu": "Aliados de China y rivales de EE.UU.",
    "neutral_ambos": "Neutrales respecto de ambos",
}
with open(os.path.join(HERE, "alignment_groups_strict.md"), "w", encoding="utf8") as f:
    f.write("# Grupos geopolíticos estrictos\n\n")
    f.write("Muestra: 186 países con ONU, seguridad y comercio disponibles para ambos ejes. ")
    f.write("Cada dimensión pesa 1/3. Se omiten las inclinaciones débiles.\n\n")
    f.write("Cortes por inclinación neta `eje_EEUU - eje_China`: fuerte EE.UU. >= 0.45; ")
    f.write("neutral [-0.15, 0.15); fuerte China < -0.45.\n\n")
    f.write("Nota: neutral significa equidistancia neta entre las dos potencias, no necesariamente ")
    f.write("bajo compromiso bilateral con ambas.\n\n")
    for idx, key in enumerate(group_order):
        part = groups[groups.grupo_estricto == key]
        f.write(f"## {labels[key]} ({len(part)})\n\n")
        for _, row in part.iterrows():
            f.write(f"- {row['name']} (`{row['iso3']}`): {row['net_lean_us']:.3f}\n")
        if idx < len(group_order) - 1:
            f.write("\n")
print(f"grupos estrictos -> alignment_groups_strict.csv/.md ({len(groups)} países)")

print("\n=== Top 15 eje EEUU ===");  print(df.nlargest(15, "axis_us")[["name","axis_us","axis_cn"]].to_string())
print("\n=== Top 15 eje China ===");  print(df.nlargest(15, "axis_cn")[["name","axis_us","axis_cn"]].to_string())
print("\n=== Rivales de EEUU (axis_us<0) ==="); print(df[df.axis_us<0][["name","axis_us","axis_cn"]].to_string())
print("\n=== Rivales de China (axis_cn<0) ==="); print(df[df.axis_cn<0][["name","axis_us","axis_cn"]].to_string())
casos = ["TUR","PAK","THA","SAU","VNM","IND","HUN","ARE","QAT","EGY","BRA","IDN","MEX","SGP","ARG","ISR","XKX","TWN"]
print("\n=== Casos que rompen categorías ==="); print(df.loc[[c for c in casos if c in df.index]][["name","axis_us","axis_cn","cuadrante"]].to_string())

# --------------------------------------------------------------------------------------
# 8. Scatter (matplotlib PNG). Color = net lean bins (diverging blue-gray-red, validated)
# --------------------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BINS = [(-np.inf, -0.45, "#9e2723", "China fuerte"), (-0.45, -0.15, "#dd7a6e", "inclinado a China"),
        (-0.15, 0.15, "#c2c0b8", "equidistante"), (0.15, 0.45, "#5f9be2", "inclinado a EEUU"),
        (0.45, np.inf, "#17529e", "EEUU fuerte")]
def bin_color(v):
    for lo, hi, c, _ in BINS:
        if lo <= v < hi: return c
    return "#c2c0b8"

fig, ax = plt.subplots(figsize=(13.5, 10), dpi=150)
fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
ax.axhline(0, color="#c3c2b7", lw=1.2, zorder=1); ax.axvline(0, color="#c3c2b7", lw=1.2, zorder=1)
ax.axhline(my, color="#898781", lw=0.8, ls=(0, (4, 4)), zorder=1)
ax.axvline(mx, color="#898781", lw=0.8, ls=(0, (4, 4)), zorder=1)
ax.grid(color="#e1e0d9", lw=0.5, zorder=0)

d = df.copy()
ax.scatter(d.axis_us, d.axis_cn, s=52, c=[bin_color(v) for v in d.net_lean_us],
           edgecolors="#0b0b0b", linewidths=0.45, alpha=0.95, zorder=3)

LABEL = {"USA","CHN","TWN","RUS","IRN","PRK","CUB","VEN","BLR","IND","PAK","THA","SAU","TUR",
         "HUN","ARE","QAT","EGY","BRA","IDN","MEX","SGP","ARG","ISR","XKX","JPN","KOR","PHL",
         "VNM","DEU","FRA","GBR","POL","UKR","CAN","AUS","LTU","NLD","SRB","KHM","MMR","ETH",
         "ZAF","NGA","KEN","KAZ","MLI","NER","CHL","COL","PER","URY","BOL","SLB","LKA","BGD",
         "MNG","NZL","SYR","SDN","AFG","NIC","ZWE","ERI","DJI","LAO","TKM","FSM","MYS","CZE"}
for iso, r in d.iterrows():
    if iso in LABEL:
        ax.annotate(iso, (r.axis_us, r.axis_cn), xytext=(4, 4), textcoords="offset points",
                    fontsize=6.8, color="#52514e", zorder=4)

ax.text(0.985, 0.985, "DOBLE JUEGO", transform=ax.transAxes, ha="right", va="top",
        fontsize=11, color="#898781", fontweight="bold")
ax.text(0.015, 0.985, "CAMPO CHINO", transform=ax.transAxes, ha="left", va="top",
        fontsize=11, color="#9e2723", fontweight="bold", alpha=0.75)
ax.text(0.985, 0.015, "CAMPO EEUU", transform=ax.transAxes, ha="right", va="bottom",
        fontsize=11, color="#17529e", fontweight="bold", alpha=0.75)
ax.text(0.015, 0.015, "AL MARGEN / NO ALINEADO", transform=ax.transAxes, ha="left", va="bottom",
        fontsize=11, color="#898781", fontweight="bold")

handles = [plt.Line2D([], [], marker="o", ls="", markersize=8, markeredgecolor="#0b0b0b",
                      markeredgewidth=0.4, color=c, label=l) for _, _, c, l in reversed(BINS)]
ax.legend(handles=handles, title="Inclinación neta (eje EEUU − eje China)", loc="center left",
          fontsize=8.5, title_fontsize=9, framealpha=0.9, edgecolor="#e1e0d9")
ax.set_xlabel("Eje EEUU  =  compromiso (votos ONU + seguridad + comercio) − hostilidad", fontsize=10.5)
ax.set_ylabel("Eje China  =  compromiso (votos ONU + seguridad + comercio) − hostilidad", fontsize=10.5)
ax.set_title(f"Alineamiento con EEUU y con China, {len(df)} países completos (2022–2025)",
             fontsize=14, fontweight="bold", pad=14, color="#0b0b0b")
ax.text(0.5, -0.085, "Líneas punteadas: mediana mundial de cada eje. Cero: la hostilidad documentada supera todo el compromiso medido.  "
        "Pesos: ⅓ votos ONU + ⅓ seguridad + ⅓ comercio − hostilidad.  Fuentes: Voeten (2022–24) · SIPRI TIV (2020–25) · FMI DOTS (2022–24) · tropas, tratados, sanciones y disputas (codificadas, ago-2026).",
        transform=ax.transAxes, ha="center", fontsize=7.2, color="#898781")
for s in ax.spines.values(): s.set_color("#c3c2b7")
ax.tick_params(colors="#52514e", labelsize=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "alignment_scatter.png"), bbox_inches="tight", facecolor="#fcfcfb")
print("\nscatter -> alignment_scatter.png")

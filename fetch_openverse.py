import json, sys, urllib.request, urllib.parse, os, time, re
sys.stdout.reconfigure(encoding="utf-8")
UA = "FahadAlMedathDemo/1.0 (afnan@attarse.com)"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")
os.makedirs(OUT, exist_ok=True)
Q = {
 "p01": "LED light bulb E27", "p02": "LED panel light ceiling", "p03": "LED downlight recessed", "p04": "LED flood light",
 "p05": "emergency light twin spot", "p06": "copper electrical wire roll", "p07": "electrical cable coil", "p08": "electrical cable reel drum",
 "p09": "flexible cable cord black", "p10": "armoured cable", "p11": "double socket outlet UK", "p12": "light switch white",
 "p13": "USB wall socket outlet", "p14": "double light switch", "p15": "circuit breaker MCB", "p16": "RCD residual current device",
 "p17": "consumer unit distribution board", "p18": "Siemens circuit breaker", "p19": "wire stripper", "p20": "Fluke multimeter",
 "p21": "electrician tool kit", "p22": "voltage tester pen", "p23": "smart light switch", "p24": "smart plug",
 "p25": "Philips Hue bulb", "p26": "ceiling fan", "p27": "exhaust fan", "p28": "solar panel", "p29": "solar inverter",
 "p30": "power strip surge protector", "p31": "UK plug BS 1363", "p32": "electrical conduit PVC pipes", "p33": "junction box electrical",
 "p34": "electrical insulation tape",
}
IDX = {}
if len(sys.argv) > 1:
    only = []
    for arg in sys.argv[1:]:
        pid, q, idx = arg.split("=")
        Q[pid] = q; IDX[pid] = int(idx); only.append(pid)
else:
    only = list(Q)

def get(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

cpath = os.path.join(OUT, "credits.json")
credits = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
for pid in only:
    q = Q[pid]; idx = IDX.get(pid, 0)
    try:
        data = json.loads(get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "by,by-sa,cc0,pdm", "page_size": 12, "mature": "false"})))
        res = [r for r in data.get("results", []) if r.get("url", "").lower().split("?")[0].endswith((".jpg", ".jpeg", ".png"))]
        if not res:
            print(pid, "NO RESULT", q); time.sleep(3.2); continue
        r = res[min(idx, len(res) - 1)]
        url = r["url"]
        if "staticflickr.com" in url:
            url = re.sub(r"_[bcz]\.jpg$", "_z.jpg", url)
        blob = get(url, 60)
        ext = "png" if url.lower().endswith(".png") else "jpg"
        for old in ("jpg", "png"):
            op = os.path.join(OUT, f"{pid}.{old}")
            if os.path.exists(op): os.remove(op)
        open(os.path.join(OUT, f"{pid}.{ext}"), "wb").write(blob)
        credits[pid] = {"title": r.get("title", ""), "page": r.get("foreign_landing_url", ""), "license": f"CC {r.get('license','').upper()} {r.get('license_version','')}".strip(),
                        "artist": (r.get("creator") or "")[:80], "source": r.get("source", ""), "query": q, "bytes": len(blob)}
        print(pid, ext, len(blob), r.get("source"), "|", r.get("title", "")[:60], "|", credits[pid]["license"])
    except Exception as e:
        print(pid, "ERROR", e)
    time.sleep(3.2)
json.dump(credits, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

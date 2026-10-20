"""Builds photos.js (data URIs, downsized) and _sheet.html (contact sheet for review) from ./photos."""
import os, json, base64, io, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "photos")
credits = json.load(open(os.path.join(P, "credits.json"), encoding="utf-8")) if os.path.exists(os.path.join(P, "credits.json")) else {}
try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None
out = {}; total = 0
for f in sorted(os.listdir(P)):
    pid, ext = os.path.splitext(f)
    if ext.lower() not in (".jpg", ".jpeg", ".png"): continue
    raw = open(os.path.join(P, f), "rb").read()
    mime = "image/jpeg"
    if Image:
        im = Image.open(io.BytesIO(raw)); im = ImageOps.exif_transpose(im).convert("RGB")
        w, h = im.size; s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((520, 520), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=78, optimize=True); raw = b.getvalue()
    elif ext.lower() == ".png":
        mime = "image/png"
    out[pid] = f"data:{mime};base64," + base64.b64encode(raw).decode(); total += len(raw)
open(os.path.join(HERE, "photos.js"), "w", encoding="utf-8").write("<style>.pimg img.pic,.gallery .main img.pic,.cartline .thumb img.pic,.gallery .thumbs img.pic{width:100%;height:100%;object-fit:cover;display:block}.pimg img.pic{border-radius:0}</style>\n<script>\nconst PHOTOS=" + json.dumps(out) + ";\nconst PHOTO_CREDITS=" + json.dumps({k: {kk: credits[k].get(kk, "") for kk in ("title", "artist", "license", "page", "source")} for k in credits if k in out}, ensure_ascii=False) + ";\n</script>\n")
tiles = "".join(f'<figure><img src="{out[k]}"><figcaption><b>{k}</b> {credits.get(k,{}).get("title","")[:40]}<br><small>{credits.get(k,{}).get("license","")} · {credits.get(k,{}).get("source","")}</small></figcaption></figure>' for k in sorted(out))
open(os.path.join(HERE, "_sheet.html"), "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><style>body{{font:12px sans-serif;margin:10px;background:#fff}}.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}}figure{{margin:0}}img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;border:1px solid #ccc}}figcaption{{height:40px;overflow:hidden}}</style></head><body><div class="g">{tiles}</div></body></html>')
print("photos", len(out), "bytes", total, "pillow", bool(Image))

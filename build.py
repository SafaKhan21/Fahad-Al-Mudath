"""Assembles the deployable pages from src.html + photos.js.

  site/index.html  standalone page (Vercel, GitHub Pages, LAN server)
  index.html       same page without the outer <html>/<head>, used for the Claude artifact

Run:  python build.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MARKER = '<div id="overlay"></div>\n'

src = open(os.path.join(HERE, "src.html"), encoding="utf-8").read()
photos = open(os.path.join(HERE, "photos.js"), encoding="utf-8").read()
if src.count(MARKER) != 1:
    raise SystemExit("src.html must contain exactly one overlay div")
page = src.replace(MARKER, MARKER + photos)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)

title_end = page.index("</title>") + len("</title>")
standalone = (
    '<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    + page[:title_end] + "\n</head>\n<body>\n" + page[title_end:] + "\n</body>\n</html>\n"
)
os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
open(os.path.join(HERE, "site", "index.html"), "w", encoding="utf-8").write(standalone)
print("built index.html and site/index.html")

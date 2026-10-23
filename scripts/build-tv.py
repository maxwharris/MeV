#!/usr/bin/env python3
"""Build the TV (.wgt) index.html from the source mockup.

Source:  work/mockups/index-app.html   (modern CSS, used for the demo)
Output:  tizen/MaxHome/index.html       (Chromium-69 safe + embedded fonts)

Conversions for the 2020 TV engine (Chromium 69):
  - clamp(a,b,c)  -> c            (fixed sizing; the canvas is a fixed 1920x1080)
  - flex `gap`    -> margins      (flex gap is Chrome 84+)
  - inset:0       -> longhand     (inset shorthand is Chrome 87+)
  - tighten vertical rhythm so the home fits 1080
  - embed Tinos (Times New Roman clone) + Cousine (Courier clone); the TV has neither
Run:  python3 scripts/build-tv.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "work/mockups/index-app.html").read_text()

# 1) clamp(a,b,c) -> c
src = re.sub(r'clamp\(\s*[^,()]+,\s*[^,()]+,\s*([^()]+?)\s*\)', lambda m: m.group(1), src)

# 2) neutralise flex gaps (grid column-gap/row-gap are fine on 69 and untouched)
for g in ("gap:.28em", "gap:26px", "gap:30px", "gap:28px", "gap:20px", "gap:.6em"):
    src = src.replace(g, "gap:0")

# 3) inset:0 -> longhand
src = src.replace("inset:0", "top:0;left:0;right:0;bottom:0")

# 4) tighten vertical rhythm to fit 1080 (clamp maxes were a touch tall)
for a, b in [("--vpad:54px", "--vpad:48px"),
             (".hero{margin-top:40px}", ".hero{margin-top:30px}")]:
    if a not in src:
        print("WARN spacing token not found:", a)
    src = src.replace(a, b)

# 5) embed fonts + margin substitutes for the neutralised gaps, injected before </style>
inject = """
  /* ---- embedded fonts (TV has no Times/Courier) ---- */
  @font-face{font-family:"Tinos";src:url("fonts/tinos.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
  @font-face{font-family:"Tinos";src:url("fonts/tinos-bold.woff2") format("woff2");font-weight:700;font-style:normal;font-display:swap}
  @font-face{font-family:"Cousine";src:url("fonts/cousine.woff2") format("woff2");font-weight:400;font-style:normal;font-display:swap}
  /* ---- flex-gap substitutes for the old engine ---- */
  .glyphs button + button{margin-left:26px}
  .clock .mer{margin-left:.18em}
  .cell .idx{margin-right:30px}
  .mrow .midx{margin-right:28px}
  .gitem .gidx{margin-right:20px}
  .vtitle .count{margin-left:.6em}
"""
src = src.replace("</style>", inject + "</style>", 1)

# 6) prefer the embedded faces
src = src.replace('"Times New Roman", Times, Georgia, serif', '"Tinos","Times New Roman",Times,serif')
src = src.replace('"Courier New", Courier, ui-monospace, monospace', '"Cousine","Courier New",Courier,monospace')

out = ROOT / "tizen/MaxHome/index.html"
out.write_text(src)

# report residual unsafe CSS (false positive on column-gap is fine)
bad = [m for m in re.findall(r'clamp\(|inset:0|aspect-ratio|backdrop-filter', src)]
print(f"wrote {out}  ({len(src)} bytes)  residual-unsafe={bad}")

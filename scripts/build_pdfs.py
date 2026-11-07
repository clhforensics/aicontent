#!/usr/bin/env python3
"""Build printable PDF editions from the canonical Markdown articles.

Requires: pip install markdown weasyprint
"""
from pathlib import Path
import sys
import html
import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "politics" / "2026-midterms"
FILES = [
    "01-morning-executive-brief",
    "02-national-and-missouri-feature",
    "03-republican-post-election-assessment",
    "04-missouri-early-warning-signals",
]

EXTRA_FILES = [
    "sports/basketball/the-nba-is-winning-the-numbers-game",
    "culture/hip-hop/how-hip-hop-learned-to-sell-danger",
]

CSS = """
@page {
  size: Letter;
  margin: 0.82in 0.82in 0.78in 0.82in;
  @bottom-right { content: counter(page); font: 9px Georgia,serif; color: #77818b; }
}
* { box-sizing: border-box; }
img { max-width: 100%; height: auto; display: block; margin: 14px auto; break-inside: avoid; }
body { font-family: Georgia, 'Liberation Serif', serif; color: #202a37; font-size: 11pt; line-height: 1.54; }
h1 { font-size: 27pt; line-height:1.12; letter-spacing:-.6px; color:#162638; border-top: 6px solid #bd8c47; padding-top: 17px; margin: 10px 0 18px; }
h2 { font-family: 'Liberation Sans', Arial, sans-serif; font-size:14pt; margin: 24px 0 8px; color:#1d3c53; border-bottom: 1px solid #d7dee4; padding-bottom: 5px; break-after: avoid; }
h3 { font-family: 'Liberation Sans',Arial,sans-serif; font-size:11.5pt; margin:18px 0 7px; color:#283b4d; break-after:avoid; }
p { margin: 0 0 12px; orphans: 3; widows: 3; }
em { color:#485664; }
blockquote { margin: 16px 0; background:#edf2f5; border-left:4px solid #bd8c47; padding: 9px 14px; font-size: 9.2pt; font-family:'Liberation Sans',Arial,sans-serif; break-inside: avoid; }
blockquote p:last-child { margin-bottom:0; }
table { width: 100%; border-collapse: collapse; font-family:'Liberation Sans',Arial,sans-serif; font-size: 9pt; margin: 13px 0 18px; }
th { background: #1b354a; color:#fff; text-align:left; padding: 7px 9px; }
td { padding: 7px 9px; border-bottom: 1px solid #dde3e7; vertical-align: top; }
tr:nth-child(even) td { background:#f3f5f6; }
tr { break-inside: avoid; }
a { color: #245f87; text-decoration: none; overflow-wrap:anywhere; }
ul,ol { margin: 0 0 13px; padding-left:22px; }
li { margin-bottom:6px; }
hr { border:0; border-top:2px solid #c6ccd1; margin:22px 0; }
code { font-family: monospace; font-size: 90%; }
"""

def build(slug):
    directory = ROOT if slug in EXTRA_FILES else FOLDER
    src = directory / (slug + ".md")
    out = directory / (slug + ".pdf")
    source = src.read_text(encoding="utf-8")
    body = markdown.markdown(source, extensions=["tables", "fenced_code", "sane_lists"])
    # Use file URL as base for relative links. HTML has no external stylesheets.
    doc = "<!DOCTYPE html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + body + "</body></html>"
    HTML(string=doc, base_url=str(src.parent)).write_pdf(str(out))
    print(f"Created {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")

if __name__ == "__main__":
    for slug in (sys.argv[1:] or FILES + EXTRA_FILES):
        if slug not in FILES + EXTRA_FILES:
            raise SystemExit(f"Unknown article: {slug}")
        build(slug)

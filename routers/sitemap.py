"""Sitemap.xml route for search engines."""
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

# All public tool pages — Google indexes these
URLS = [
    # Main
    {"loc": "https://toollab.ca", "priority": "1.0", "changefreq": "weekly"},
    {"loc": "https://toollab.ca/pricing", "priority": "0.8", "changefreq": "monthly"},
    # PDF tools
    {"loc": "https://toollab.ca/pdf/", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "https://toollab.ca/pdf/summarize", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/pdf/chat", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/pdf/to-word", "priority": "0.9", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/pdf/split", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/pdf/rotate", "priority": "0.7", "changefreq": "monthly"},
    # Image tools
    {"loc": "https://toollab.ca/image/", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "https://toollab.ca/image/palette", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/image/convert", "priority": "0.9", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/image/resize", "priority": "0.8", "changefreq": "monthly"},
    # Voice
    {"loc": "https://toollab.ca/voice/", "priority": "0.8", "changefreq": "monthly"},
    # QR & Text & Calc
    {"loc": "https://toollab.ca/qr/", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/text/", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "https://toollab.ca/calc/", "priority": "0.7", "changefreq": "monthly"},
    # Blog
    {"loc": "https://toollab.ca/blog", "priority": "0.9", "changefreq": "weekly"},
]

# Add blog articles to sitemap
from routers.blog import ARTICLES as BLOG_ARTICLES
for slug in BLOG_ARTICLES:
    URLS.append({
        "loc": f"https://toollab.ca/blog/{slug}",
        "priority": "0.8",
        "changefreq": "monthly",
    })


@router.get("/sitemap.xml")
async def sitemap(request: Request):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in URLS:
        xml += "  <url>\n"
        xml += f"    <loc>{url['loc']}</loc>\n"
        xml += f"    <priority>{url['priority']}</priority>\n"
        xml += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        xml += "  </url>\n"
    xml += "</urlset>"
    return PlainTextResponse(xml, media_type="application/xml")

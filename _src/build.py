#!/usr/bin/env python3
"""Builds the static multi-page site from _src/site.html.

Source of truth: _src/site.html (single-file SPA, all pages as <section class="page">).
Output: index.html + one folder per route (/services/chatting/index.html, ...),
each containing only its own page, with its own title, description, canonical and JSON-LD.
Run from anywhere:  python3 _src/build.py
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "site.html"
BASE = "https://zion-management.eu"
OG_IMAGE = BASE + "/assets/og-zion.jpg"
EMAIL = "neo@zion-management.eu"
INSTAGRAM = "https://www.instagram.com/neomngmt"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_data import PATHS, META, CRUMBS, SERVICE_SCHEMA  # noqa: E402

try:
    from cz_data import CZ_PAGES, CZ_META, CZ_STRINGS, CZ_SHELL  # noqa: E402
except ImportError:
    CZ_PAGES, CZ_META, CZ_STRINGS, CZ_SHELL = [], {}, {}, {}

LEGACY = {"chatting.html": "chatting", "marketing.html": "marketing", "photoshooting.html": "photoshooting",
          "services.html": "services", "contact.html": "contact", "referral.html": "referral",
          "refer-a-creator.html": "refer-a-creator"}


def esc(s):
    return html.escape(s, quote=True)


def url_for(key, lang="en"):
    p = PATHS[key]
    if lang == "cz":
        return "/cz" + (p if p != "/" else "/")
    return p


def split_source(src):
    i_title = src.index("<title>")
    m = re.search(r'<meta name="twitter:image"[^>]*>\n', src)
    i_after_head_meta = m.end()
    head_pre = src[:i_title]
    rest = src[i_after_head_meta:]
    main_open = rest.index('<main id="app">')
    shell_top = rest[:main_open]
    main_close = rest.index("</main>")
    main_html = rest[main_open + len('<main id="app">'):main_close]
    shell_bottom = rest[main_close + len("</main>"):]
    pages = {}
    starts = [(m.group(1), m.start(), m.end())
              for m in re.finditer(r'<section class="page(?: active)?" id="page-([\w-]+)" data-page="[\w-]+">', main_html)]
    for n, (key, st, en) in enumerate(starts):
        stop = starts[n + 1][1] if n + 1 < len(starts) else len(main_html)
        body = main_html[en:stop]
        body = body[:body.rindex("</section>")]
        pages[key] = body
    return head_pre, shell_top, pages, shell_bottom


def faq_items(page_html):
    out = []
    for m in re.finditer(r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*<div class="faq-body">(.*?)</div>\s*</details>', page_html, re.S):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        out.append((html.unescape(q), html.unescape(a)))
    return out


def jsonld(key, lang, meta, page_html):
    url = BASE + url_for(key, lang)
    graph = []
    if key == "home":
        graph.append({
            "@type": "Organization", "@id": BASE + "/#org", "name": "ZION",
            "url": BASE + "/", "logo": OG_IMAGE, "email": EMAIL,
            "sameAs": [INSTAGRAM],
            "areaServed": ["US", "CZ"],
            "description": META["home"]["desc"],
        })
        graph.append({"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "ZION",
                      "publisher": {"@id": BASE + "/#org"}, "inLanguage": "cs" if lang == "cz" else "en"})
        faqs = faq_items(page_html)
        if faqs:
            graph.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    else:
        crumbs = CRUMBS.get(key, [("home", None)])
        items = [{"@type": "ListItem", "position": 1, "name": "ZION", "item": BASE + url_for("home", lang)}]
        trail = [c for c in crumbs if c[0] != "home"]
        for n, (ck, label) in enumerate(trail, start=2):
            if lang == "cz":
                label = {"Services": "Služby", "Referral": "Doporučení"}.get(label, label)
            items.append({"@type": "ListItem", "position": n, "name": label or meta["h1"],
                          "item": BASE + url_for(ck, lang)})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": meta["h1"], "item": url})
        graph.append({"@type": "BreadcrumbList", "itemListElement": items})
    if key.startswith("blog-"):
        graph.append({"@type": "BlogPosting", "headline": meta["h1"], "description": meta["desc"],
                      "mainEntityOfPage": url, "image": OG_IMAGE,
                      "author": {"@type": "Organization", "name": "ZION", "url": BASE + "/"},
                      "publisher": {"@id": BASE + "/#org"} if False else {"@type": "Organization", "name": "ZION", "url": BASE + "/"},
                      "inLanguage": "cs" if lang == "cz" else "en"})
    if key in SERVICE_SCHEMA:
        graph.append({"@type": "Service", "name": SERVICE_SCHEMA[key], "description": meta["desc"], "url": url,
                      "provider": {"@type": "Organization", "name": "ZION", "url": BASE + "/"},
                      "areaServed": ["US", "CZ"]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def head_block(key, lang, meta, page_html):
    url = BASE + url_for(key, lang)
    t, d = esc(meta["title"]), esc(meta["desc"])
    og_type = "article" if key.startswith("blog-") else "website"
    alts = ""
    if key in CZ_PAGES:
        alts = (f'<link rel="alternate" hreflang="en" href="{BASE}{url_for(key, "en")}">\n'
                f'<link rel="alternate" hreflang="cs" href="{BASE}{url_for(key, "cz")}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{BASE}{url_for(key, "en")}">\n')
    legacy = ""
    if key == "home" and lang == "en":
        mapping = {k: PATHS[k] for k in PATHS if k != "home"}
        legacy = ("<script>(function(){var m=" + json.dumps(mapping) +
                  ";var h=location.hash.slice(1);if(h&&m[h]&&location.pathname==='/'){location.replace(m[h]);}})();</script>\n")
    return (f"<title>{t}</title>\n"
            f'<meta name="description" content="{d}">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<meta name="robots" content="index,follow,max-image-preview:large">\n'
            f"{alts}"
            f'<meta property="og:type" content="{og_type}">\n'
            f'<meta property="og:site_name" content="ZION">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{OG_IMAGE}">\n'
            f'<meta property="og:locale" content="{"cs_CZ" if lang == "cz" else "en_US"}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{t}">\n'
            f'<meta name="twitter:description" content="{d}">\n'
            f'<meta name="twitter:image" content="{OG_IMAGE}">\n'
            f"{legacy}"
            f'<script type="application/ld+json">{jsonld(key, lang, meta, page_html)}</script>\n')


def rewrite_links(h, key, lang):
    prefix = "/cz" if lang == "cz" else ""

    def href(m):
        name = m.group(1)
        if name == "home":
            return f'href="{prefix}/"'
        if name in PATHS:
            if lang == "cz" and name not in CZ_PAGES:
                return f'href="{PATHS[name]}"'
            return f'href="{url_for(name, lang)}"'
        if name in ("faq", "stats", "irl"):
            return f'href="#{name}"' if key == "home" else f'href="{prefix}/#{name}"'
        return m.group(0)
    h = re.sub(r'href="#([\w-]+)"', href, h)

    def loc(m):
        name = m.group(1)
        return f"location.href='{url_for(name, lang) if name in PATHS else '/'}'"
    h = re.sub(r"location\.hash='([\w-]+)'", loc, h)
    h = re.sub(r'(["\'(])assets/', r"\1/assets/", h)
    return h


ROUTER_RE = re.compile(r"<script>\s*\(function\(\)\{\s*const PAGES = \[.*?</script>", re.S)


def router_script(key):
    return ('<script>document.addEventListener("DOMContentLoaded",function(){'
            f'if(window.__setActiveNav)window.__setActiveNav("{key}");'
            'var h=location.hash.slice(1);if(h){var el=document.getElementById(h);'
            'if(el)setTimeout(function(){el.scrollIntoView({behavior:"smooth"});},250);}});</script>')


def build_page(key, lang, head_pre, shell_top, page_html, shell_bottom):
    meta = (CZ_META if lang == "cz" else META)[key]
    body_html = page_html
    top, bottom = shell_top, shell_bottom
    if lang == "cz":
        from cz_data import translate  # noqa
        body_html = translate(body_html)
        top = translate(top)
        bottom = translate(bottom)
    section = f'\n<section class="page active" id="page-{key}" data-page="{key}">{body_html}</section>\n'
    doc = head_pre + head_block(key, lang, meta, body_html) + top + '<main id="app">' + section + "</main>" + bottom
    doc = ROUTER_RE.sub(lambda _m: router_script(key), doc)
    en_href = url_for(key, "en")
    cz_href = url_for(key, "cz") if key in CZ_PAGES else "/cz/"
    sw = ('<div class="lang-switch" role="group" aria-label="Language">'
          f'<a href="{en_href}" hreflang="en" lang="en"{" class=\"is-on\"" if lang == "en" else ""}>EN</a>'
          '<span class="sl">/</span>'
          f'<a href="{cz_href}" hreflang="cs" lang="cs"{" class=\"is-on\"" if lang == "cz" else ""}>CZ</a></div>')
    doc = doc.replace('<div class="nav-right">', '<div class="nav-right">' + sw, 1)
    if key in CZ_PAGES:
        other = url_for(key, "en" if lang == "cz" else "cz")
        label, hl = ("English", "en") if lang == "cz" else ("Čeština", "cs")
        link = f'<span class="sep">·</span><a href="{other}" hreflang="{hl}" lang="{hl}">{label}</a>'
        for cls in ("footer-policy-links", "footer-links"):
            doc = re.sub(r'(<div class="%s">.*?)(</div>)' % cls, lambda m: m.group(1) + link + m.group(2), doc, count=1, flags=re.S)
    doc = rewrite_links(doc, key, lang)
    if lang == "cz":
        doc = doc.replace('<html lang="en">', '<html lang="cs">', 1)
    return doc


def out_path(key, lang):
    p = url_for(key, lang).strip("/")
    return ROOT / "index.html" if p == "" else ROOT / p / "index.html"


def main():
    src = SRC.read_text()
    head_pre, shell_top, pages, shell_bottom = split_source(src)
    missing = [k for k in PATHS if k not in pages]
    if missing:
        sys.exit("pages missing in source: %s" % missing)
    urls = []
    for key in PATHS:
        for lang in ("en",) + (("cz",) if key in CZ_PAGES else ()):
            doc = build_page(key, lang, head_pre, shell_top, pages[key], shell_bottom)
            op = out_path(key, lang)
            op.parent.mkdir(parents=True, exist_ok=True)
            op.write_text(doc)
            urls.append((BASE + url_for(key, lang), key, lang))
    # sitemap
    prio = {"home": "1.0", "services": "0.9", "apply": "0.9", "about": "0.8", "success-stories": "0.8"}
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u, key, lang in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        if key in CZ_PAGES:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{url_for(key, "en")}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="cs" href="{BASE}{url_for(key, "cz")}"/>')
        lines.append(f"    <priority>{prio.get(key, '0.6')}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n")

    # legacy standalone files -> redirect stubs, plus a 404 page
    for fname, key in LEGACY.items():
        dest = BASE + url_for(key)
        (ROOT / fname).write_text(
            '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<title>{esc(META[key]["title"])}</title>'
            f'<meta http-equiv="refresh" content="0;url={dest}">'
            f'<link rel="canonical" href="{dest}"><meta name="robots" content="noindex,follow">'
            f'</head><body><p>This page moved to <a href="{dest}">{dest}</a>.</p>'
            f'<script>location.replace("{url_for(key)}")</script></body></html>\n')
    (ROOT / "404.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Page not found | ZION</title><meta name="robots" content="noindex">'
        '<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#07090a;color:#f2f5f0;font-family:Inter,system-ui,sans-serif;text-align:center}'
        'a{color:#39e673}h1{font-weight:300;font-size:44px;margin:0 0 12px}p{color:#8fa39a;margin:0 0 22px}</style></head>'
        '<body><div><h1>Page not found</h1><p>This page does not exist (anymore).</p><a href="/">Back to ZION</a></div></body></html>\n')
    print("built", len(urls), "pages")


if __name__ == "__main__":
    main()

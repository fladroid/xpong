#!/usr/bin/env python3
"""
xpong · health_check.py
Provera infrastrukture i stanja projekta.
Pokretanje: python3 health_check.py
"""

import json
import re
import socket
import subprocess
import urllib.request
from pathlib import Path

XPONG_HOME = Path(__file__).resolve().parent          # /home/balsam/xpong
WEB_HOME   = Path("/var/www/xpong")
DOMAIN     = "xpong.opik.net"
EXPECTED_IP = "130.61.37.60"
LIVE_URL   = f"https://{DOMAIN}"

OK   = "\033[92m✅\033[0m"
WARN = "\033[93m⚠️ \033[0m"
ERR  = "\033[91m❌\033[0m"
HDR  = "\033[1;96m"
RST  = "\033[0m"

def hdr(title):
    print(f"\n{HDR}{'═'*52}{RST}")
    print(f"{HDR}  {title}{RST}")
    print(f"{HDR}{'═'*52}{RST}")

def row(icon, label, value=""):
    print(f"  {icon}  {label:<32} {value}")

# ── 1. Git — docs repo (xpong) ───────────────────────────────────────
def check_git_docs():
    hdr("1. Git — docs repo (xpong)")
    if not XPONG_HOME.exists():
        row(ERR, "Putanja", f"NE POSTOJI: {XPONG_HOME}")
        return None
    result = subprocess.run(
        ["git", "-C", str(XPONG_HOME), "status", "--short"],
        capture_output=True, text=True, timeout=10
    )
    lines = result.stdout.strip().splitlines()
    if not lines:
        row(OK, "Working tree", "čist")
    else:
        row(WARN, "Uncommitted promene", f"{len(lines)} fajlova")
        for l in lines:
            print(f"       {l}")

    log = subprocess.run(
        ["git", "-C", str(XPONG_HOME), "log", "--oneline", "-3"],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()
    print(f"\n  Zadnja 3 commita (xpong):")
    for l in log.splitlines():
        print(f"    {l}")

    return subprocess.run(
        ["git", "-C", str(XPONG_HOME), "log", "--oneline", "-1"],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()

# ── 2. Git — web repo (xpongweb) ─────────────────────────────────────
def check_git_web():
    hdr("2. Git — web repo (xpongweb)")
    if not WEB_HOME.exists():
        row(ERR, "Putanja", f"NE POSTOJI: {WEB_HOME}")
        return None
    result = subprocess.run(
        ["git", "-C", str(WEB_HOME), "status", "--short"],
        capture_output=True, text=True, timeout=10
    )
    lines = result.stdout.strip().splitlines()
    if not lines:
        row(OK, "Working tree", "čist")
    else:
        row(WARN, "Uncommitted promene", f"{len(lines)} fajlova")
        for l in lines:
            print(f"       {l}")

    log = subprocess.run(
        ["git", "-C", str(WEB_HOME), "log", "--oneline", "-3"],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()
    print(f"\n  Zadnja 3 commita (xpongweb):")
    for l in log.splitlines():
        print(f"    {l}")

    return subprocess.run(
        ["git", "-C", str(WEB_HOME), "log", "--oneline", "-1"],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()

# ── 3. Sinhronizacija docs ↔ web (oznaka sesije) ─────────────────────
def check_sync(docs_head, web_head):
    hdr("3. Sinhronizacija docs ↔ web")
    def sess_tag(head):
        m = re.search(r"\bs\d+(\.\d+)?\b", head or "")
        return m.group(0) if m else "?"
    docs_sess = sess_tag(docs_head)
    web_sess  = sess_tag(web_head)
    if docs_sess == "?" or web_sess == "?":
        row(WARN, "Oznaka sesije", f"nije prepoznata (docs='{docs_sess}', web='{web_sess}')")
    elif docs_sess == web_sess:
        row(OK, "Repo-i sinhronizovani", f"{docs_sess}")
    else:
        row(WARN, "Repo-i NISU sinhronizovani", f"docs={docs_sess}, web={web_sess}")

# ── 4. Struktura web fajlova ──────────────────────────────────────────
def check_structure():
    hdr("4. Struktura web fajlova")
    expected = [
        "index.html", "about.html",
        "game.html", "game.js", "pong-core.js",
        "xray.html", "xray.js",
        "rl1.html", "rl1.js",
        "xpong.css", "app.js", "favicon.svg",
        "data/concepts.json", ".gitignore",
    ]
    for f in expected:
        p = WEB_HOME / f
        row(OK, f) if p.exists() else row(ERR, f, "NEDOSTAJE")

# ── 5. concepts.json — validnost ─────────────────────────────────────
def check_concepts_json():
    hdr("5. concepts.json — validnost")
    p = WEB_HOME / "data" / "concepts.json"
    if not p.exists():
        row(ERR, "Fajl", "NE POSTOJI")
        return
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        row(OK, "JSON parsiran", f"{len(data)} sekcija")
        for section in data:
            n = len(data[section]) if isinstance(data[section], list) else "?"
            row(OK, f"  sekcija '{section}'", f"{n} kartica")
    except Exception as e:
        row(ERR, "JSON parsiranje", str(e))

# ── 6. DNS ─────────────────────────────────────────────────────────────
def check_dns():
    hdr("6. DNS")
    try:
        ip = socket.gethostbyname(DOMAIN)
        row(OK if ip == EXPECTED_IP else WARN, DOMAIN,
            f"→ {ip}" + ("" if ip == EXPECTED_IP else f" (očekivano {EXPECTED_IP})"))
    except Exception as e:
        row(ERR, DOMAIN, str(e))

# ── 7. Live site ──────────────────────────────────────────────────────
def check_live_site():
    hdr("7. Live site")
    try:
        req = urllib.request.Request(LIVE_URL, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            row(OK, "HTTPS status", str(resp.status))
    except Exception as e:
        row(ERR, "HTTPS status", str(e))
        return

    try:
        with urllib.request.urlopen(f"{LIVE_URL}/app.js", timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        m = re.search(r"XP_VERSION\s*=\s*['\"]([^'\"]+)['\"]", content)
        live_version = m.group(1) if m else None
        row(OK if live_version else WARN, "XP_VERSION (live)", live_version or "nije pronađen")
    except Exception as e:
        row(ERR, "app.js fetch", str(e))
        return

    local_app = WEB_HOME / "app.js"
    if local_app.exists() and live_version:
        local_content = local_app.read_text(encoding="utf-8", errors="replace")
        m2 = re.search(r"XP_VERSION\s*=\s*['\"]([^'\"]+)['\"]", local_content)
        local_version = m2.group(1) if m2 else None
        if local_version:
            row(OK if local_version == live_version else WARN, "Live vs lokalno",
                local_version if local_version == live_version else f"live={live_version}, lokalno={local_version}")

# ── 8. Apache vhost-ovi ────────────────────────────────────────────────
def check_apache():
    hdr("8. Apache vhost-ovi")
    for conf in ("xpong.opik.net.conf", "xpong.opik.net-le-ssl.conf"):
        p = Path("/etc/apache2/sites-enabled") / conf
        row(OK, conf, "enabled") if (p.exists() or p.is_symlink()) else row(WARN, conf, "nije u sites-enabled")

# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{HDR}{'█'*52}{RST}")
    print(f"{HDR}  XPONG · Health Check{RST}")
    print(f"{HDR}{'█'*52}{RST}")

    docs_head = check_git_docs()
    web_head  = check_git_web()
    check_sync(docs_head, web_head)
    check_structure()
    check_concepts_json()
    check_dns()
    check_live_site()
    check_apache()

    print(f"\n{HDR}{'═'*52}{RST}")
    print(f"{HDR}  Health check završen.{RST}")
    print(f"{HDR}{'═'*52}{RST}\n")

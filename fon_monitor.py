"""
FON Katedra za IS Monitor
--------------------------
Pokreće se jednom (GitHub Actions ga poziva po rasporedu).
State se čuva u seen_posts.json koji Actions commit-uje u repo.
"""

import requests
import json
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

TARGET_URL = "https://is.fon.bg.ac.rs/"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]   # čita iz GitHub Secrets
NTFY_SERVER = "https://ntfy.sh"
STATE_FILE  = "seen_posts.json"

# ─── STATE ────────────────────────────────────────────────────────────────────

def load_seen() -> set:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)

# ─── NTFY ─────────────────────────────────────────────────────────────────────

def send_ntfy(title: str, body: str, url: str = None):
    headers = {
        "Title":    title.encode("utf-8"),
        "Priority": "high",
        "Tags":     "school,bell",
    }
    if url:
        headers["Click"] = url
    r = requests.post(
        f"{NTFY_SERVER}/{NTFY_TOPIC}",
        data=body.encode("utf-8"),
        headers=headers,
        timeout=10,
    )
    r.raise_for_status()
    print(f"  ✓ ntfy: {title}")

# ─── SCRAPING ─────────────────────────────────────────────────────────────────

def fetch_posts() -> list[dict]:
    r = requests.get(
        TARGET_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    posts = []

    for article in soup.find_all("article"):
        title_tag = article.find(
            ["h1", "h2", "h3"],
            class_=lambda c: c and "entry-title" in c
        ) or article.find(["h1", "h2", "h3"])

        if not title_tag:
            continue

        a_tag  = title_tag.find("a")
        title  = title_tag.get_text(strip=True)
        link   = a_tag["href"] if a_tag else TARGET_URL
        time_t = article.find("time")
        date   = time_t.get_text(strip=True) if time_t else "?"

        posts.append({
            "id":    link.rstrip("/"),
            "title": title,
            "date":  date,
            "url":   link,
        })

    return posts

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Proveravam {TARGET_URL}...")
    seen  = load_seen()
    posts = fetch_posts()
    print(f"  Pronađeno {len(posts)} postova na stranici, {len(seen)} zapamćenih.")

    # Prvo pokretanje — samo zapamti, ne šalji notifikacije
    if not seen:
        print("  Prvo pokretanje, pamtim postojeće postove...")
        save_seen({p["id"] for p in posts})
        return

    new_posts = [p for p in posts if p["id"] not in seen]

    if not new_posts:
        print("  Ništa novo.")
        return

    print(f"  🆕 {len(new_posts)} novi post(ovi)!")
    for post in new_posts:
        print(f"     • {post['date']} — {post['title']}")
        send_ntfy(
            title=f"IS FON: {post['title']}",
            body=f"Objavljeno: {post['date']}",
            url=post["url"],
        )
        seen.add(post["id"])

    save_seen(seen)


if __name__ == "__main__":
    main()

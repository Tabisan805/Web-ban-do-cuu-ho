import schedule, time, json, os
from crawler import crawl_all_sources
from analyzer import classify_event
from location_extractor import extract_location
from uploader import post_event

CACHE_FILE = "bot/cache.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"processed_links": []}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def job():
    print("🔁 Đang quét nguồn dữ liệu...")
    cache = load_cache()
    processed = set(cache.get("processed_links", []))
    posts = crawl_all_sources()

    # Lọc trùng link ngay khi thu thập
    unique_posts = []
    seen_links = set()
    for p in posts:
        if not p.get("link"): continue
        if p["link"] in seen_links: continue
        seen_links.add(p["link"])
        unique_posts.append(p)

    for p in unique_posts:
        if p["link"] in processed:
            continue

        classification = classify_event(p["text"], p["source_type"])
        if not classification:
            continue

        loc = extract_location(p["text"])
        if not loc:
            continue

        event = {
            **classification,
            **loc,
            "name": p["text"][:40] + "...",
            "description": p["text"],
            "source": p["source_type"],
            "link": p["link"]
        }
        post_event(event)
        processed.add(p["link"])

    cache["processed_links"] = list(processed)[-1000:]
    save_cache(cache)
    print("✅ Hoàn tất chu kỳ quét!")

schedule.every(10).minutes.do(job)

print("🤖 Bot cứu hộ đang chạy định kỳ mỗi 10 phút...")
while True:
    schedule.run_pending()
    time.sleep(60)

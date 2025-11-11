import concurrent.futures
import requests
from bs4 import BeautifulSoup
from facebook_scraper import get_posts
import json

def crawl_news(url, pages=3):
    """Crawl nhiều trang tin tức để lấy bài cũ hơn."""
    results = []
    for i in range(1, pages + 1):
        try:
            page_url = f"{url}?p={i}"
            res = requests.get(page_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                if len(title) > 25:
                    link = a["href"]
                    if not link.startswith("http"):
                        link = requests.compat.urljoin(url, link)
                    results.append({
                        "text": title,
                        "link": link,
                        "source_type": "news"
                    })
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy {page_url}: {e}")
    return results

def crawl_facebook(page_url, max_pages=3):
    """Crawl nhiều trang bài viết Facebook (1-2 tuần gần nhất)."""
    page_name = page_url.split("/")[-1]
    posts = []
    try:
        for post in get_posts(page_name, pages=max_pages, options={"comments": False, "reactors": False}):
            if post.get("text"):
                posts.append({
                    "text": post["text"],
                    "link": post["post_url"],
                    "source_type": "facebook",
                    "time": str(post.get("time"))
                })
    except Exception as e:
        print(f"⚠️ Lỗi Facebook {page_name}: {e}")
    return posts

def crawl_all_sources():
    with open("bot/sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    results = []

    def handle_source(s):
        try:
            if s["type"] == "news":
                return crawl_news(s["url"])
            elif s["type"] == "facebook":
                return crawl_facebook(s["url"])
        except Exception as e:
            print(f"⚠️ Lỗi lấy {s['name']}: {e}")
            return []

    # 🔥 Chạy song song nhiều nguồn
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(handle_source, s) for s in sources]
        for f in concurrent.futures.as_completed(futures):
            results.extend(f.result())

    print(f"✅ Đã thu thập {len(results)} bài viết.")
    return results

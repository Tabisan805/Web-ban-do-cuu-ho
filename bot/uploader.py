import requests
from datetime import datetime

def post_event(event):
    payload = {
        "name": event.get("name") or event.get("type", "Sự kiện"),
        "category": event["category"],
        "type": event["type"],
        "address": event["address"],
        "lat": event["lat"],
        "lng": event["lng"],
        "time": datetime.now().isoformat(),
        "description": event.get("description", ""),
        "source": event.get("source", "")
    }
    try:
        r = requests.post("http://localhost:5000/api/events", json=payload, timeout=5)
        print(f"✅ Gửi: {payload['name']} ({payload['category']}) - {payload['address']}")
    except Exception as e:
        print("❌ Lỗi gửi dữ liệu:", e)

import re
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="rescue_bot")

def extract_location(text):
    """
    Tìm địa danh trong câu (theo mẫu 'ở ...' hoặc 'tại ...'),
    kể cả có phần trong ngoặc hoặc kèm 'tỉnh', 'thành phố'.
    Trả về tọa độ GPS (lat, lng).
    """
    # Bắt cụm: ở Quy Nhơn (tỉnh Gia Lai), tại thành phố Huế,...
    match = re.search(r"(?:ở|tại)\s+([A-ZĐ][\w\s,().-]+)", text)
    if not match:
        return None

    raw_address = match.group(1).strip()
    # Loại bỏ từ thừa như 'thành phố', 'tỉnh' nếu cần
    address = re.sub(r'\b(thành phố|tỉnh|huyện|xã|phường)\b', '', raw_address, flags=re.IGNORECASE).strip()

    # Nếu có ngoặc, nối phần trong ngoặc vào
    if '(' in raw_address and ')' in raw_address:
        inner = re.search(r'\(([^)]+)\)', raw_address)
        if inner:
            address = f"{address}, {inner.group(1)}"

    try:
        loc = geolocator.geocode(address + ", Việt Nam", timeout=10)
        if loc:
            return {"address": address, "lat": loc.latitude, "lng": loc.longitude}
    except Exception as e:
        print("⚠️ Không tìm được tọa độ:", e)

    return None

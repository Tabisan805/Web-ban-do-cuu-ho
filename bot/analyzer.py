def classify_event(text, source_type):
    text_lower = text.lower()

    # Nếu là báo chí → tin tức
    if source_type == "news":
        if any(k in text_lower for k in ["bão", "áp thấp", "mưa lớn", "lũ", "cảnh báo", "thiên tai"]):
            return {"category": "news", "type": "Cảnh báo bão/lũ"}
        return None

    # Nếu là Facebook → cứu hộ
    if source_type == "facebook":
        if any(k in text_lower for k in ["cứu hộ", "cứu trợ", "ngập", "cháy", "mất tích", "kêu gọi"]):
            if "cháy" in text_lower: return {"category": "rescue", "type": "Cháy"}
            if "ngập" in text_lower or "lũ" in text_lower: return {"category": "rescue", "type": "Ngập/Lũ"}
            if "mất tích" in text_lower: return {"category": "rescue", "type": "Mất tích"}
            if "bão" in text_lower: return {"category": "news", "type": "Bão"}  # fallback
            return {"category": "rescue", "type": "Cứu hộ khác"}
    return None

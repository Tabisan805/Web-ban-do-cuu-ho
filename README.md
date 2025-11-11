<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   WEB BẢN ĐỒ CỨU HỘ VIÊT NAM
</h2>
<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---
## 1. Giới thiệu hệ thống
Bản đồ Cứu hộ Khẩn cấp là một hệ thống thu thập, phân tích và hiển thị dữ liệu sự kiện khẩn cấp (cháy nổ, ngập lụt, tai nạn, thiên tai, mất điện...) tại Việt Nam.
Mục tiêu của dự án là:
- 🧩 Tự động thu thập thông tin từ báo chí, mạng xã hội và các nguồn cộng đồng.
- 🗺️ Trực quan hóa vị trí sự kiện trên bản đồ số toàn quốc.
- ⚙️ Tạo nền tảng dữ liệu mở phục vụ nghiên cứu, cảnh báo và cứu hộ.

Hệ thống hoạt động theo mô hình Client–Server–Bot:
- Bot thu thập và xử lý dữ liệu thô.
- Server Flask cung cấp API và giao diện hiển thị.
- Frontend bản đồ (Leaflet) trình bày dữ liệu tương tác cho người dùng.

### Bot Modular
Bot được thiết kế modular như sau:
| File | Chức năng |
|:-----|:----------|
|crawler.py	|Thu thập tin tức và bài đăng Facebook liên quan đến cứu hộ, thiên tai, tai nạn... | |
|analyzer.py	|Phân loại nội dung thu thập được thành 2 nhóm: news (tin tức) và rescue (cứu hộ). | |
|location_extractor.py	|Dùng NLP để rút trích địa danh, chuẩn hóa tên tỉnh/thành, và tìm tọa độ GPS (sử dụng API geocoding). | |
|scheduler.py	|Chạy bot theo lịch định kỳ (cronjob), tổng hợp dữ liệu mới, tránh trùng lặp, và kiểm tra dữ liệu lỗi. | |
|uploader.py	|Gửi dữ liệu đã chuẩn hóa đến API Flask /api/events để cập nhật lên bản đồ. | |

Luồng hoạt động của modular
```
crawler.py → analyzer.py → location_extractor.py → uploader.py → Flask API
```

### Server
Sử dụng Flask để Xử lý API RESTful /api/events (GET, POST).

Lưu trữ và truy xuất dữ liệu từ cơ sở dữ liệu SQLite.

### Giao diện bản đồ cứu hộ
Hiển thị dữ liệu bằng Leaflet.js kết hợp VietMap API được tự động cập nhật mỗi 30 giây.

Sử dụng các Marker để hiển thị thể hiện loại sự kiện bằng màu sắc khác nhau:
- 🔴 Cháy nổ

- 🔵 Ngập lụt

- 🟠 Tai nạn

- 🟢 Cứu hộ khác


### Hạn chế hiện tại

- Phụ thuộc nguồn dữ liệu: Bot chỉ thu thập được các bài viết và tin tức có thể truy cập công khai; những thông tin từ nhóm kín hoặc mạng xã hội hạn chế sẽ bị bỏ sót.
- Độ chính xác địa điểm: Một số bài viết không cung cấp địa chỉ cụ thể, dẫn đến tọa độ GPS có thể chưa hoàn toàn chính xác.
- Cập nhật thời gian thực còn hạn chế: Dữ liệu trên bản đồ được tải lại theo chu kỳ (mặc định 30 giây), chưa thực sự “live” từng giây.
- Khả năng phân loại sự kiện: Hiện tại bot phân loại chỉ dựa trên từ khóa; những bài viết phức tạp có thể bị phân loại nhầm.
---
## 2. Công nghệ sử dụng
<div align="center">
    
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000)](#)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=fff)](#)
</div>


## 3. Các bước cài đặt 

### 🛠️ 3.1. Yêu cầu hệ thống

- ☕ **Python:** Phiên bản ≥ 3.9
- 💻 **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux.
- 📡 **Kết nối mạng:** Bắt buộc để bot thu thập tin tức từ web và Facebook, đồng thời tải bản đồ VietMap.
- 💾 **Bộ nhớ:** ≥ 4GB RAM, dung lượng trống tối thiểu 500MB  

---

### 📥3.2. Các bước cài đặt

### 🧰 Cài môi trường Python
Yêu cầu:

- Python ≥ 3.9
- pip (Python Package Manager)

Cài đặt các thư viện cần thiết:
```
pip install flask flask-cors sqlalchemy requests beautifulsoup4 underthesea

```


Cấu trúc thư mục dự án:
```
project/
│
├── app.py                      # Flask server chính
├── database.py                 # Khởi tạo và kết nối cơ sở dữ liệu
├── bot/
│   ├── crawler.py              # Thu thập tin tức & bài đăng mạng xã hội
│   ├── analyzer.py             # Phân loại nội dung thành rescue/news
│   ├── location_extractor.py   # Rút trích địa danh & toạ độ
│   ├── scheduler.py            # Chạy định kỳ, quản lý luồng dữ liệu
│   └── uploader.py             # Gửi dữ liệu lên API Flask
├── templates/
│   └── admin.html              # Giao diện bản đồ cứu hộ
├── static/
│   ├── css/style.css           # Giao diện & bố cục
│   └── js/map.js               # Xử lý bản đồ, cập nhật marker
└── README.md


```
### 🏗 Bước 2: Biên dịch mã nguồn
Mở terminal và điều hướng đến thư mục src của dự án:
```
cd path/to/project/src
```
### ▶️ Bước 3: Khởi tạo cơ sở dữ liệu
Khởi động Server
```
python database.py
```
Sẽ tạo file data/events.db tự động.

### 🏗 Bước 4: Chạy server 
Mở terminal và sử dụng: 
```
python app.py
```
Truy cập:
- Trang bản đồ quản trị: http://127.0.0.1:5000/admin

Bạn mở 1 terminal song song và chạy:
```
python bot/scheduler.py
```
Bot sẽ:
- Gọi crawler.py để thu thập bài viết mới.
- Gọi analyzer.py để lọc bài liên quan cứu hộ.
- Dùng location_extractor.py để tìm địa danh và toạ độ.
- Dùng uploader.py để đẩy dữ liệu hợp lệ lên API Flask.

---
## 4. Liên hệ
- **Sinh viên thực hiện:** **Lã Việt Hoàng**
- **Khoa Công nghệ thông tin – Đại học Đại Nam**  
- 🌐 Website: [https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)  
- 📧 Email: [lahoangprotknl@gmail.com]
- 📱 Fanpage: [AIoTLab - FIT DNU](https://www.facebook.com/DNUAIoTLab)

---

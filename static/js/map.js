const map = L.map('map').setView([16.047, 108.206], 6);
const vietmapToken = "75be3e7457da81b80159b030c38e3a33c40332fcb365c243";

L.tileLayer(`https://maps.vietmap.vn/tm/{z}/{x}/{y}.png?apikey=${vietmapToken}`, {
  maxZoom: 18,
  attribution: '&copy; Vietmap'
}).addTo(map);

let markers = [];

// --- Load dữ liệu ---
async function loadEvents() {
  const city = document.getElementById("citySelect").value;
  const url = city ? `/api/events?city=${encodeURIComponent(city)}` : "/api/events";
  const res = await fetch(url);
  const events = await res.json();
  updateTable(events);
  updateMap(events);
  focusCity(city);
}

// --- Cập nhật bảng ---
function updateTable(events) {
  const tbody = document.getElementById("eventBody");
  tbody.innerHTML = "";
  events.forEach((e, i) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${i + 1}</td>
      <td>${escapeHtml(e.name || "")}</td>
      <td>${escapeHtml(e.type || "")}</td>
      <td>${escapeHtml(e.address || "")}</td>
      <td>${new Date(e.time).toLocaleString()}</td>
    `;
    row.onclick = () => focusMarker(i);
    tbody.appendChild(row);
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, m => ({
    "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"
  }[m]));
}

// --- Hiển thị marker ---
function updateMap(events) {
  markers.forEach(m => map.removeLayer(m));
  markers = [];

  events.forEach((e, i) => {
    if (!e.lat || !e.lng) return;

    const color = e.type?.includes("cháy") ? "red" :
                  e.type?.includes("ngập") ? "blue" :
                  e.type?.includes("tai nạn") ? "orange" : "green";

    const icon = L.divIcon({
      html: `<div style="background:${color};width:14px;height:14px;border-radius:50%;border:2px solid white;"></div>`,
      className: ''
    });

    // --- Icon nguồn (source) ---
    const src = (e.source || "").toLowerCase();
    let srcIcon = "🌐";
    if (src.includes("facebook")) srcIcon = "🔵";
    else if (src.includes("news")) srcIcon = "📰";
    else if (src.includes("user") || src.includes("người")) srcIcon = "👤";
    else if (src.includes("system") || src.includes("tự động")) srcIcon = "🛰️";

    // --- Link nguồn ---
    const linkHtml = e.link
      ? `<a href="${escapeHtml(e.link)}" target="_blank" rel="noopener" style="color:#1565c0;text-decoration:none;">🔗 Xem bài gốc</a>`
      : `<span style="color:gray;">Không có liên kết</span>`;

    const popupHtml = `
      <div style="min-width:200px;">
        <b>${escapeHtml(e.name || "Sự cố không tên")}</b><br>
        <i>${escapeHtml(e.type || "Không rõ loại")}</i><br>
        📍 ${escapeHtml(e.address || "Không rõ địa chỉ")}<br>
        🕒 ${new Date(e.time).toLocaleString()}<br>
        ${srcIcon} <b>Nguồn:</b> ${escapeHtml(e.source || "Không xác định")}<br>
        ${linkHtml}
      </div>
    `;

    const marker = L.marker([e.lat, e.lng], { icon })
      .addTo(map)
      .bindPopup(popupHtml)
      .on("click", () => showInfo(e));

    markers.push(marker);
  });
}



// --- Mở panel chi tiết ---
function showInfo(e) {
  document.getElementById("infoName").textContent = e.name || "Không rõ";
  document.getElementById("infoType").textContent = e.type || "Không xác định";
  document.getElementById("infoAddress").textContent = e.address || "Chưa có";
  document.getElementById("infoTime").textContent = new Date(e.time).toLocaleString();
  document.getElementById("infoDesc").textContent = e.description || "Không có mô tả chi tiết.";
  const src = (e.source || "").toLowerCase();
  let srcIcon = "🌐";
  if (src.includes("facebook")) srcIcon = "🔵";
  else if (src.includes("news")) srcIcon = "📰";
  else if (src.includes("user") || src.includes("người")) srcIcon = "👤";
  else if (src.includes("system") || src.includes("tự động")) srcIcon = "🛰️";

  document.getElementById("infoSource").innerHTML =
    `${srcIcon} ${escapeHtml(e.source || "Không xác định")}`;

  // --- Link gốc ---
  document.getElementById("infoLink").innerHTML = e.link
    ? `<a href="${escapeHtml(e.link)}" target="_blank" rel="noopener" style="color:#1565c0;text-decoration:none;">🔗 Mở bài viết gốc</a>`
    : `<span style="color:gray;">Không có liên kết nguồn</span>`;


  document.getElementById("infoPanel").classList.remove("hidden");
}

function closeInfo() {
  document.getElementById("infoPanel").classList.add("hidden");
}

// --- Zoom đến marker ---
function focusMarker(index) {
  if (markers[index]) {
    map.setView(markers[index].getLatLng(), 13);
    markers[index].openPopup();
  }
}

// --- Zoom theo thành phố ---
function focusCity(city) {
  const positions = {
    "Hà Nội": [21.0285, 105.8542],
    "TP.HCM": [10.776, 106.700],
    "Đà Nẵng": [16.047, 108.206],
    "Cần Thơ": [10.045, 105.746]
  };
  if (city && positions[city]) map.setView(positions[city], 12);
  else map.setView([16.047, 108.206], 6);
}

function toggleList() {
  const tableContainer = document.getElementById("table-container");
  tableContainer.classList.toggle("hidden");

  // Gọi lại invalidateSize sau khi hiệu ứng flex hoàn tất
  setTimeout(() => map.invalidateSize(), 350);
}



// --- Cập nhật định kỳ ---
setInterval(loadEvents, 30000);
loadEvents();

# Tuyến nội dung và giọng đã chốt

| Tên gọi | Là gì | Độ dài | Giọng |
|---|---|---|---|
| **PODCAST** | Đời sống thực tế cho người đi làm 22–35 tuổi, dựa trên sách hiện đại (kiểu Better Version). Kịch bản: `podcast/` | 15–20 phút | Giọng thật của chủ kênh, thu bằng điện thoại → `cong-cu/xu_ly_giong.py` → `dung_video.py --giong` |
| **CHUYỆN** | Truyện hư cấu công sở / gia đình / ân tình / nhân quả. YouTube bản đầy đủ, TikTok chia tập | 8–12 phút | `Ngọc Huyền` (VieNeu, `--may vieneu`) |
| **KINH** | Sách cổ: video dài theo chủ đề (`kenh-2-sach-thuc-tinh/video-dai/`) và diễn giải từng chương (`dao-duc-kinh/`) | 6–20 phút | `Thiền Tâm Đức`, `Thanh Bình` |

Ưu tiên hiện tại: PODCAST và CHUYỆN.

## Nhạc nền đã chốt (SÁCH và KINH)

Ba bản trong `assets/nhac/tinh/`, dùng xoay vòng: `nature-meditation`, `piano-reflections`, `smooth-meditation` (nguồn Mixkit, miễn phí bản quyền).
Chạy `dung_video.py --nhac ../assets/nhac/tinh` — máy tự xáo thứ tự theo seed, cắt bớt âm cao, nén cho đều và đặt nhạc ở mức -30 LUFS (giọng -16).
Bản cũ "Forest Treasure" đã loại vì chói, nghe đêm khó chịu.

# Tuyến nội dung và giọng đã chốt

| Tên gọi | Là gì | Độ dài | Giọng |
|---|---|---|---|
| **SÁCH** | Một nỗi khổ của người xem + một cuốn sách (kiểu Better Version). Kịch bản: `kenh-2-sach-thuc-tinh/video-dai/` | 15–25 phút | Giọng thật của chủ kênh, thu bằng điện thoại → `cong-cu/xu_ly_giong.py` → `dung_video.py --giong` |
| **CHUYỆN** | Truyện hư cấu công sở / gia đình / ân tình / nhân quả. YouTube bản đầy đủ, TikTok chia tập | 8–12 phút | `Ngọc Huyền` (VieNeu, `--may vieneu`) |
| **KINH** | Diễn giải sách cổ từng chương (Đạo Đức Kinh 81 chương…) — tạm gác | 6–10 phút | `Thiền Tâm Đức` (Đạo Đức Kinh), `Thanh Bình` (bộ sau) |

Ưu tiên hiện tại: SÁCH và CHUYỆN.

## Nhạc nền đã chốt (SÁCH và KINH)

Ba bản trong `assets/nhac/tinh/`, dùng xoay vòng: `nature-meditation`, `piano-reflections`, `smooth-meditation` (nguồn Mixkit, miễn phí bản quyền).
Chạy `dung_video.py --nhac ../assets/nhac/tinh` — máy tự xáo thứ tự theo seed, cắt bớt âm cao, nén cho đều và đặt nhạc ở mức -30 LUFS (giọng -16).
Bản cũ "Forest Treasure" đã loại vì chói, nghe đêm khó chịu.

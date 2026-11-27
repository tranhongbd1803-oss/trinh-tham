# Tuyến nội dung và giọng đã chốt

| Tên gọi | Là gì | Ai làm | Giọng |
|---|---|---|---|
| **PODCAST** | Chỉ nhóm chủ đề ăn khách: cảm xúc và tâm lý (giận, tự ti, trì hoãn, kỷ luật) và các mốc tuổi (25, 35). Kịch bản: `podcast/` | Claude viết, chủ kênh thu âm | Giọng thật, thu bằng điện thoại → `cong-cu/xu_ly_giong.py` → `dung_video.py --giong` |
| **SÁCH** | Công thức Better Version: mỗi video một cuốn sách, tiêu đề bán vấn đề của người xem; ưu tiên mảng tỉnh thức, Đạo gia, Phật gia; xếp theo "tủ sách"; âm thanh đăng lại làm podcast Spotify/Apple. Kịch bản: `kenh-2-sach-thuc-tinh/video-dai/` | Claude làm trọn | Giọng máy `Thiền Tâm Đức`, `Thanh Bình` |
| **CHUYỆN** | Truyện hư cấu công sở / gia đình / ân tình / nhân quả. YouTube bản đầy đủ, TikTok chia tập | Claude làm trọn | Giọng máy `Ngọc Huyền` |
| **KINH** | Diễn giải sách cổ từng chương (`dao-duc-kinh/`) — tạm gác | Claude làm trọn | Giọng máy `Thiền Tâm Đức` |

Ưu tiên hiện tại: PODCAST và CHUYỆN.

## Nhạc nền đã chốt (SÁCH và KINH)

Ba bản trong `assets/nhac/tinh/`, dùng xoay vòng: `nature-meditation`, `piano-reflections`, `smooth-meditation` (nguồn Mixkit, miễn phí bản quyền).
Chạy `dung_video.py --nhac ../assets/nhac/tinh` — máy tự xáo thứ tự theo seed, cắt bớt âm cao, nén cho đều và đặt nhạc ở mức -30 LUFS (giọng -16).
Bản cũ "Forest Treasure" đã loại vì chói, nghe đêm khó chịu.

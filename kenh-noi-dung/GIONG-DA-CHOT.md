# Tuyến nội dung và giọng đã chốt

**Kênh YouTube:** Nâng Cấp Góc Nhìn (`@nangcapgocnhin`) — gồm 2 series: GÓC NHÌN (tuyến PODCAST) và ĐỌC CHẬM (tuyến SÁCH). Kênh CHUYỆN riêng, chờ tên.

| Tên gọi | Là gì | Ai làm | Giọng |
|---|---|---|---|
| **PODCAST** | Chỉ nhóm chủ đề ăn khách: cảm xúc và tâm lý (giận, tự ti, trì hoãn, kỷ luật) và các mốc tuổi (25, 35). Kịch bản: `podcast/` | Claude viết, chủ kênh thu âm | Giọng thật, thu bằng điện thoại → `cong-cu/xu_ly_giong.py` → `dung_video.py --giong` |
| **SÁCH** | Công thức Better Version: mỗi video một cuốn sách, tiêu đề bán vấn đề của người xem; ưu tiên mảng tỉnh thức, Đạo gia, Phật gia; xếp theo "tủ sách"; âm thanh đăng lại làm podcast Spotify/Apple. Kịch bản: `kenh-2-sach-thuc-tinh/video-dai/` | Claude làm trọn | Giọng máy `Thiền Tâm Đức`, `Thanh Bình` |
| **CHUYỆN** | Truyện hư cấu công sở / gia đình / ân tình / nhân quả. YouTube bản đầy đủ, TikTok chia tập | Claude làm trọn | Giọng máy `Ngọc Huyền` |
| **KINH** | Diễn giải sách cổ từng chương (`dao-duc-kinh/`) — tạm gác | Claude làm trọn | Giọng máy `Thiền Tâm Đức` |

Ưu tiên hiện tại: PODCAST và CHUYỆN.

## Nhạc nền đã chốt (28/11/2026)

Dùng ba bản **tự tạo bằng máy** trong `assets/nhac/tu-tao/` (`tu-tao-am`, `tu-tao-mo`, `tu-tao-chuong`), xoay vòng linh hoạt.
Tạo lại bằng `python cong-cu/tao_nhac_nen.py --ra assets/nhac/tu-tao`. Chạy dựng với `--nhac ../assets/nhac/tu-tao`.

**Không dùng nhạc Mixkit nữa:** video SÁCH 001 bị YouTube báo "Claimed content" (bài "Ajudar Com Sabedoria" – Glauber Ouro) do một trong ba bản Mixkit cũ (`assets/nhac/tinh/`).

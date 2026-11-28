# Khung video kênh Tiệm Vui Vẻ

Sáu khung 1080×1920 nền trong suốt trong `khung/`: đỏ Tết, bạc hà, cam đào, vàng bơ, tím mơ, hồng phấn. Xem nhanh ở `xem-truoc-6-mau.png`.

## Dùng trong CapCut
1. Tạo dự án tỉ lệ 9:16, đưa video vào. Kéo video lên nửa trên màn hình (phần hình thấy được là từ mép trên xuống khoảng 60% chiều cao).
2. Bấm **Lớp phủ → Thêm lớp phủ**, chọn file khung PNG, kéo cho phủ kín màn hình. Khung nằm trên video.
3. Thêm **Văn bản** vào trong thẻ: tiêu đề 2 dòng chữ đậm, mô tả 2–3 dòng chữ thường.
4. Chữ chỉ đặt trong thẻ. Phần dưới thẻ và mép phải sẽ bị nút và chú thích của TikTok che.

## Tạo khung có sẵn chữ hoặc thêm màu mới
```
node khung.js --mau do-tet --tieu-de "DÒNG 1|DÒNG 2" --mo-ta "Mô tả ngắn" --ra ten-file.png
```
Thêm bộ màu: sửa bảng `MAU` ở đầu file `khung.js` rồi chạy `node khung.js`.

## Công thức video affiliate của kênh (chốt 28/11/2026)

- **Khung:** đỏ Tết (`khung/khung-do-tet.png`) cho hàng Tết; các màu khác dùng theo mùa/sản phẩm.
- **Giọng:** VieNeu `Trúc Ly`, bản "thanh" (nâng tông 6%, làm sáng âm, nén nhẹ, đọc sát nhịp).
- **Độ dài:** 35–40 giây. Lời thoại 170–195 chữ (đã tính tốc độ x1.15).
- **Lời thoại:** câu móc trong 5 giây đầu (kiểu "Trời ơi! …") → cầm/ngửi → cắn/nhai → chấm/kết hợp → dịp dùng (Tết, bia, biếu) → lợi ích chốt → **câu kêu gọi cuối: "Bấm ngay vào giỏ hàng ở góc trái màn hình để đặt mua nha!"**
- **Giọng điệu:** giữ từ đệm thân mật ("luôn á", "nha", "trời ơi" trong câu). **Không** dùng tiếng cảm thán rời ("Ưm!", "Ôi,", "hứ") và **không** dùng tiếng cười máy `[cười]` — nghe bị lố.
- **Tốc độ đọc:** x1.15 sau khi nâng tông.
- **Nhãn cuối video:** 3–4 giây cuối hiện nhãn vàng "Bấm giỏ hàng góc trái" ở góc trái dưới thẻ chữ.
- **Hình:** 12–15 đoạn cắt 2–3 giây, xếp đúng theo lời thoại; hình chỉ nằm ở 60% phía trên, thẻ chữ ở dưới.
- **Âm nền:** tiếng ăn (nhai nhẹ làm nền ở đoạn xé–nhai–chấm; tiếng cắn, mở lon, rót bia, cụng ly đặt đúng chữ). Không ghép nhạc — chọn nhạc thịnh hành trong TikTok lúc đăng.
- **Trên thẻ:** tiêu đề 2 dòng (tên món + lợi ích), mô tả 2–3 dòng. Giá, mã giảm, "bấm giỏ hàng" để ở chú thích TikTok.
- **Giao kèm mỗi video:** chú thích TikTok (2–3 phương án, có câu nhắc bấm giỏ hàng) và bộ hashtag (3–4 thẻ rộng + 3–4 thẻ đúng món + 1–2 thẻ mùa vụ). Gửi dạng chữ ngay trong tin nhắn để chủ kênh sao chép trên điện thoại.

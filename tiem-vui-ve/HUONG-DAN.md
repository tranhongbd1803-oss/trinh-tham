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

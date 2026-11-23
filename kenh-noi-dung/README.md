# Xưởng nội dung — 2 kênh YouTube/TikTok

**Phân vai:** Claude sản xuất từ A đến Z (chọn thể loại, viết kịch bản, nhân bản biến tấu, chọn cảnh, dựng video). **Anh/chị:** duyệt và đăng.

| | Kênh 1 — Chuyện đời | Kênh 2 — Sách thức tỉnh |
|---|---|---|
| Tên gợi ý | **Nghe Chuyện Đời** · Chuyện Công Sở Kể Đêm · Góc Kể Chuyện | **Đọc Chậm** · Tĩnh Thư · Một Chương Mỗi Tối |
| Nội dung | Truyện audio hư cấu: công sở, gia đình, ân tình, nhân quả | Diễn giải sách cổ theo chương: Đạo Đức Kinh → Pháp Cú → Trang Tử… |
| Hình | Tay người đang làm gì đó (nấu ăn, pha trà, làm gốm…), không lộ mặt | Thiên nhiên tĩnh, trà, thư pháp, mưa, nến |
| Tiếng | Giọng kể + nhạc nền nhẹ | Giọng trầm chậm + đàn tranh/sáo |
| Nhịp đăng | 1 dài/ngày + 2 Shorts/ngày | 3 chương/tuần + 1 Short/ngày |

## Cấu trúc thư mục

```
kenh-noi-dung/
├── README.md                       ← bạn đang đọc
├── CHIEN-LUOC.md                   ← định vị, lịch đăng, kiếm tiền, LUẬT để không bị tắt kiếm tiền
├── kenh-1-chuyen-doi/
│   ├── ma-tran-bien-tau.json       ← "cà chua → cam, quýt, mít, dừa": các trục để đổi
│   ├── kich-ban-goc/               ← kịch bản gốc (quả mẹ)
│   ├── bien-tau/                   ← 80 đề cương nhân bản (4 thể loại × 20), có bảng _bang-*.md
│   └── kich-ban-hoan-chinh/        ← kịch bản biến tấu đã viết đầy đủ, sẵn dựng
├── kenh-2-sach-thuc-tinh/
│   └── dao-duc-kinh/               ← kế hoạch 84 video + chương 1, 2 viết đầy đủ
├── cong-cu/
│   ├── nhan_ban.py                 ← máy nhân bản kịch bản
│   ├── dung_video.py               ← máy dựng video (giọng + cảnh + nhạc + phụ đề)
│   └── ghep_tong_hop.py            ← ghép 81 chương thành 1 video dài + mốc thời gian
└── assets/                         ← bỏ clip nền & nhạc vào đây (không đẩy lên git)
```

## Đã có sẵn để duyệt

| File | Loại | Độ dài |
|---|---|---|
| `kenh-1-chuyen-doi/kich-ban-goc/001-co-ke-toan-va-ban-du-toan.md` | Gốc · lật kèo công sở | ~9 phút + Short 70s |
| `kenh-1-chuyen-doi/kich-ban-hoan-chinh/001-03-cau-ky-thuat-vien-it.md` | Biến tấu từ 001 | ~7 phút + Short 60s |
| `kenh-1-chuyen-doi/bien-tau/` | 80 đề cương (001-xx, 101-xx, 201-xx, 301-xx) | chờ viết |
| `kenh-2-sach-thuc-tinh/dao-duc-kinh/chuong-01.md`, `chuong-02.md` | Diễn giải | ~7 phút + Short |
| `kenh-2-sach-thuc-tinh/dao-duc-kinh/ke-hoach-series.md` | Lịch 84 video | — |

So sánh 001 và 001-03 để thấy cách "nhân bản": **cùng xương sống 7 nhịp** (móc câu → vết thương → 3 lần chèn ép → hạt giống bí mật → lật ngược → hậu quả → đúc kết) nhưng khác bối cảnh, người kể, bí mật, cách kết — nghe là hai câu chuyện khác hẳn nhau.

## Quy trình mỗi video (anh/chị chỉ làm bước 4–5)

1. **Claude** chọn đề cương trong `bien-tau/` → viết thành kịch bản hoàn chỉnh vào `kich-ban-hoan-chinh/`.
2. **Claude** chọn cảnh nền + nhạc + seed, ghi vào đầu kịch bản.
3. **Máy dựng** ra video dài 16:9 + Short 9:16 + file phụ đề `.srt`.
4. **Anh/chị duyệt**: nghe thử, xem tiêu đề A/B, báo sửa (nếu có).
5. **Anh/chị đăng**: dán tiêu đề, mô tả, upload `.srt`, đặt lịch.

## Chạy máy dựng (trên máy tính của anh/chị)

Môi trường đám mây của Claude đang bị chặn mạng tới dịch vụ giọng đọc, nên bước tạo giọng chạy trên máy anh/chị (hoặc mở mạng cho môi trường này, Claude dựng luôn).

```bash
# 1 lần: cài Python 3.10+, ffmpeg, rồi:
pip install -r kenh-noi-dung/cong-cu/requirements.txt

cd kenh-noi-dung/cong-cu
# Video dài YouTube
python dung_video.py --kich-ban ../kenh-1-chuyen-doi/kich-ban-goc/001-co-ke-toan-va-ban-du-toan.md \
  --voice vi-VN-HoaiMyNeural --toc-do -8% \
  --clips ../assets/clips/nau-an --nhac ../assets/nhac/piano.mp3 --khung 16x9 --ra ../xuat/001.mp4
# Short dọc
python dung_video.py --kich-ban ../kenh-1-chuyen-doi/kich-ban-goc/001-co-ke-toan-va-ban-du-toan.md \
  --phan ngan --clips ../assets/clips/nau-an --nhac ../assets/nhac/piano.mp3 --khung 9x16 --ra ../xuat/001-short.mp4
# Nhân bản 20 đề cương mới từ một thể loại
python nhan_ban.py --the-loai lat-keo-cong-so --goc 002 --seed 7
```

Giọng Việt có sẵn: `vi-VN-NamMinhNeural` (nam), `vi-VN-HoaiMyNeural` (nữ). Muốn giọng tự nhiên hơn: thu giọng thật hoặc dùng ElevenLabs/FPT.AI, rồi chạy với `--giong file.mp3`.

## Kho clip nền & nhạc (miễn phí, được dùng thương mại)

- Clip: **Pexels Videos**, **Pixabay Videos**, **Coverr**, **Mixkit** — tìm "cooking hands", "pouring tea", "pottery", "rain window", "calligraphy". Tải 30–50 clip/chủ đề là đủ xoay vòng hàng trăm video, máy dựng tự cắt-xáo khác nhau mỗi lần.
- Nhạc: **YouTube Audio Library** (an toàn nhất cho YouTube), **Pixabay Music**, **Mixkit Music**.
- Tốt nhất: tự quay tay mình nấu ăn / pha trà bằng điện thoại — vừa độc quyền vừa giúp kênh không bị coi là "nội dung tái sử dụng".
- ❌ Không tải video nấu ăn của kênh TikTok/YouTube khác về ghép — sẽ dính Content ID / bản quyền và mất kiếm tiền.

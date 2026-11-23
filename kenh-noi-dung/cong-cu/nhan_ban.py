#!/usr/bin/env python3
"""
Máy NHÂN BẢN kịch bản: 1 kịch bản gốc (quả cà chua) -> N đề cương biến tấu (cam, quýt, mít, dừa...).

Giữ nguyên XƯƠNG SỐNG 7 nhịp, chỉ đổi các TRỤC trong ma-tran-bien-tau.json.
Máy chọn tổ hợp sao cho các bản KHÁC NHAU NHIỀU NHẤT (không bản nào trùng quá 2 trục với bản khác),
rồi xuất mỗi bản thành 1 file đề cương .md để viết thành kịch bản đầy đủ.

Dùng:
  python nhan_ban.py --the-loai lat-keo-cong-so --so-ban 20 --goc 001 --ra ../kenh-1-chuyen-doi/bien-tau
"""
import argparse
import json
import random
import re
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
NHIP = [
    ("1. MÓC CÂU (0:00–0:20)", "Một câu mở gây sốc/tò mò, kể luôn khoảnh khắc cao trào rồi tua ngược: 'Ba tháng trước, không ai trong phòng thèm nhớ tên tôi…'"),
    ("2. NHÂN VẬT & VẾT THƯƠNG", "Giới thiệu {nhan_vat} ở {boi_canh}: hoàn cảnh, lý do họ phải nhẫn nhịn (nợ nần, con nhỏ, mẹ ốm…)."),
    ("3. BỊ CHÈN ÉP — 3 LẦN TĂNG DẦN", "{ke} {kieu}. Lần 1 nhỏ, lần 2 công khai, lần 3 chạm giới hạn. Mỗi lần kết bằng một câu đau."),
    ("4. HẠT GIỐNG BÍ MẬT", "Gài 1–2 chi tiết nhỏ khán giả để ý mà nhân vật trong truyện không: nhân vật chính {bi_mat}."),
    ("5. CAO TRÀO LẬT NGƯỢC", "Tại {cao_trao}: sự thật lộ ra. Viết chậm, nhiều thoại, cho khán giả 'hả hê'."),
    ("6. HẬU QUẢ", "Kết cục cho từng người. Kiểu kết: {ket}."),
    ("7. ĐÚC KẾT + KÊU GỌI", "1–2 câu bài học, không giảng đạo. Hỏi khán giả 1 câu để bình luận. Mời đăng ký."),
]


NHAN = {"boi_canh": "Bối cảnh", "nhan_vat_chinh": "Nhân vật chính", "ke_chen_ep": "Kẻ chèn ép",
        "kieu_chen_ep": "Kiểu chèn ép", "bi_mat": "Bí mật", "cao_trao": "Cao trào",
        "kieu_ket": "Kiểu kết", "giong_ke": "Giọng kể", "nguoi_giup": "Người giúp",
        "nguoi_duoc_giup": "Người được giúp", "viec_tot": "Việc tốt", "thoi_gian": "Thời gian",
        "cach_gap_lai": "Cách gặp lại", "xung_dot": "Xung đột", "nhan_vat_tham": "Kẻ tham",
        "nan_nhan": "Nạn nhân", "qua_bao": "Quả báo"}


def ngan(s):
    """'cô thực tập sinh mới ra trường' -> 'cô thực tập sinh' (để tiêu đề gọn)."""
    s = re.split(r"[,—(]| mới | ngoài | sắp | ít ", s)[0].strip()
    return s


def hoa(s):
    return s[:1].upper() + s[1:]


def chon_to_hop(truc, so_ban, rng, toi_da_trung=2, so_lan_thu=4000):
    ten_truc = list(truc)
    da_chon, dem = [], {t: {} for t in ten_truc}
    for _ in range(so_lan_thu):
        if len(da_chon) >= so_ban:
            break
        # ưu tiên giá trị ít được dùng để rải đều
        th = {}
        for t in ten_truc:
            vals = truc[t]
            mn = min(dem[t].get(v, 0) for v in vals)
            th[t] = rng.choice([v for v in vals if dem[t].get(v, 0) == mn])
        if all(sum(th[t] == c[t] for t in ten_truc) <= toi_da_trung for c in da_chon):
            da_chon.append(th)
            for t in ten_truc:
                dem[t][th[t]] = dem[t].get(th[t], 0) + 1
    return da_chon


def tieu_de(mau, th, rng):
    bien = {}
    for k, v in th.items():
        bien[k] = v
        bien[k + "_hoa"] = hoa(v)
    nv = th.get("nhan_vat_chinh") or th.get("nguoi_giup") or ""
    bien.update(nhan_vat_ngan=ngan(nv), nhan_vat_ngan_hoa=hoa(ngan(nv)))
    if "bi_mat" in th:
        bien["bi_mat_ngan"] = th["bi_mat"].split(" mà ")[0].split(" do ")[0]
    out = []
    for m in rng.sample(mau, min(3, len(mau))):
        try:
            out.append(m.format(**bien))
        except KeyError:
            pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ma-tran", type=Path, default=GOC / "kenh-1-chuyen-doi/ma-tran-bien-tau.json")
    ap.add_argument("--the-loai", default="lat-keo-cong-so")
    ap.add_argument("--so-ban", type=int, default=20)
    ap.add_argument("--goc", default="001", help="mã kịch bản gốc")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--ra", type=Path, default=GOC / "kenh-1-chuyen-doi/bien-tau")
    a = ap.parse_args()

    mt = json.loads(a.ma_tran.read_text(encoding="utf-8"))["the_loai"][a.the_loai]
    rng = random.Random(a.seed)
    ds, trung = [], 2
    while len(ds) < a.so_ban and trung < len(mt["truc"]):   # trục ít thì nới dần độ trùng
        ds = chon_to_hop(mt["truc"], a.so_ban, random.Random(a.seed), toi_da_trung=trung)
        trung += 1
    a.ra.mkdir(parents=True, exist_ok=True)
    muc_luc = [f"# Bảng nhân bản từ kịch bản gốc {a.goc} — {mt['ten']}\n",
               "| Mã | Bối cảnh / Nhân vật | Tiêu đề đề xuất | Trạng thái |", "|---|---|---|---|"]
    for i, th in enumerate(ds, 1):
        ma = f"{a.goc}-{i:02d}"
        tds = tieu_de(mt["mau_tieu_de"], th, rng)
        g = {"nhan_vat": th.get("nhan_vat_chinh", th.get("nguoi_giup", "")),
             "boi_canh": th.get("boi_canh", th.get("xung_dot", "")),
             "ke": th.get("ke_chen_ep", th.get("nhan_vat_tham", "")),
             "kieu": th.get("kieu_chen_ep", th.get("viec_tot", "")),
             "bi_mat": th.get("bi_mat", th.get("cach_gap_lai", "")),
             "cao_trao": th.get("cao_trao", th.get("thoi_gian", "")),
             "ket": th.get("kieu_ket", "")}
        md = [f"# Đề cương {ma}", "", f"**Gốc:** {a.goc} · **Thể loại:** {mt['ten']}", "",
              "## Tổ hợp biến tấu", ""]
        md += [f"- **{NHAN.get(k, k)}:** {v}" for k, v in th.items()]
        md += ["", "## Tiêu đề đề xuất", ""] + [f"- {t}" for t in tds]
        md += ["", "## Xương sống 7 nhịp", ""]
        for ten, mo_ta in NHIP:
            md += [f"**{ten}** — {mo_ta.format(**g)}", ""]
        md += ["## Ghi chú dựng", "",
               f"- Seed dựng gợi ý: `{rng.randrange(10**6)}` (mỗi bản một seed → kết cấu hình khác nhau)",
               "- Bản dài 8–12 phút cho YouTube; cắt nhịp 1+3+5 thành bản ngắn 60–90s cho TikTok/Shorts, dừng ở cao trào → 'Phần 2 trên kênh'."]
        (a.ra / f"{ma}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        muc_luc.append(f"| [{ma}]({ma}.md) | {g['boi_canh']} / {g['nhan_vat']} | {tds[0] if tds else ''} | đề cương |")
    (a.ra / f"_bang-{a.goc}.md").write_text("\n".join(muc_luc) + "\n", encoding="utf-8")
    print(f"✔ Tạo {len(ds)} đề cương trong {a.ra}")


if __name__ == "__main__":
    main()

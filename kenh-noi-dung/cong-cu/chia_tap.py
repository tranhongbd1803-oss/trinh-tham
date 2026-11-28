#!/usr/bin/env python3
"""
Chia một truyện thành các TẬP dọc 9:16 cho TikTok, theo các dấu [TẬP] đặt trong kịch bản.
Mỗi tập được đọc và dựng riêng; tập chưa phải cuối kết bằng lời hẹn tập sau.

  python chia_tap.py --kich-ban ../kenh-1-chuyen-doi/kich-ban-goc/001-*.md --voice "Ngọc Huyền" \
      --clips ../assets/clips/nau-an --ra-thu-muc ../xuat/chuyen --ma c001
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--kich-ban", type=Path, required=True)
ap.add_argument("--voice", default="Ngọc Huyền")
ap.add_argument("--clips", type=Path, required=True)
ap.add_argument("--nhac", type=Path, nargs="*")
ap.add_argument("--ra-thu-muc", type=Path, required=True)
ap.add_argument("--ma", required=True)
ap.add_argument("--seed", type=int, default=100)
ap.add_argument("--tang-toc", type=float, default=1.0)
a = ap.parse_args()

raw = a.kich_ban.read_text(encoding="utf-8")
m = re.search(r"<!-- DOC -->(.*?)<!-- HET DOC -->", raw, re.S)
if not m:
    sys.exit("Không thấy đoạn <!-- DOC -->")
tap = [t.strip() for t in re.split(r"\[TẬP\]", m.group(1)) if t.strip()]
n = len(tap)
a.ra_thu_muc.mkdir(parents=True, exist_ok=True)
for i, t in enumerate(tap, 1):
    dau = "" if i == 1 else f"Tập {i}.\n\n"
    cuoi = f"\n\nNghe tiếp tập {i + 1} trên kênh nhé." if i < n else ""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(f"<!-- DOC NGAN -->\n{dau}{t}{cuoi}\n<!-- HET DOC NGAN -->\n")
        tam = f.name
    ra = a.ra_thu_muc / f"{a.ma}-tap{i}-tren-{n}.mp4"
    cmd = [sys.executable, str(Path(__file__).with_name("dung_video.py")), "--may", "vieneu", "--voice", a.voice,
           "--kich-ban", tam, "--phan", "ngan", "--clips", str(a.clips), "--khung", "9x16",
           "--seed", str(a.seed + i), "--tang-toc", str(a.tang_toc), "--ra", str(ra)]
    if a.nhac:
        cmd += ["--nhac", *map(str, a.nhac)]
    print(f"— Tập {i}/{n}: {len(t.split())} chữ")
    subprocess.run(cmd, check=True)
print(f"✔ {n} tập trong {a.ra_thu_muc}")

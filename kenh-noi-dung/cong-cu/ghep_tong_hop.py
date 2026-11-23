#!/usr/bin/env python3
"""
Ghép nhiều video tập (vd 81 chương Đạo Đức Kinh) thành 1 video tổng hợp dài,
và tự sinh danh sách MỐC THỜI GIAN (chapters) để dán vào mô tả YouTube.

Dùng:
  python ghep_tong_hop.py --vao ../xuat/ddk/chuong-*.mp4 --ra ../xuat/ddk/tron-bo.mp4 \
      --ten-tap "Chương {n}"
Các video vào phải cùng khung hình/fps (đều dựng bằng dung_video.py cùng --khung là được).
"""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


def do_dai(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "json", str(p)], text=True)
    return float(json.loads(out)["format"]["duration"])


def moc(giay):
    giay = int(giay)
    h, m, s = giay // 3600, giay % 3600 // 60, giay % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vao", nargs="+", type=Path, required=True)
    ap.add_argument("--ra", type=Path, required=True)
    ap.add_argument("--ten-tap", default="Phần {n}")
    a = ap.parse_args()
    vao = sorted(a.vao, key=lambda p: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", p.name)])
    t, dong = 0.0, []
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for i, p in enumerate(vao, 1):
            f.write(f"file '{p.resolve()}'\n")
            dong.append(f"{moc(t)} {a.ten_tap.format(n=i)}")
            t += do_dai(p)
        ds = f.name
    a.ra.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", ds,
                    "-c", "copy", "-movflags", "+faststart", str(a.ra)], check=True)
    a.ra.with_suffix(".moc-thoi-gian.txt").write_text("\n".join(dong) + "\n", encoding="utf-8")
    print(f"✔ {a.ra} ({moc(t)}) — mốc thời gian: {a.ra.with_suffix('.moc-thoi-gian.txt')}")


if __name__ == "__main__":
    main()

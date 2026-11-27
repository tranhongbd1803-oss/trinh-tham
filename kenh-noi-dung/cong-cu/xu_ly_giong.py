#!/usr/bin/env python3
"""
Làm đẹp giọng thu bằng điện thoại: lọc ù/ồn nền, thêm độ dày ("nội lực"), làm rõ chữ,
nén cho giọng đều và chắc, chuẩn hoá âm lượng đúng mức YouTube.

  python xu_ly_giong.py thu-am.m4a                 # -> thu-am-dep.wav + thu-am-dep.mp3
  python xu_ly_giong.py thu-am.m4a --kieu am       # ấm, dày (mặc định) — hợp đọc sách
  python xu_ly_giong.py thu-am.m4a --kieu sang     # sáng, rõ — hợp giọng trầm bị đục
  python xu_ly_giong.py thu-am.m4a --khu-on 18     # phòng ồn: khử ồn mạnh hơn (mặc định 10)
  python xu_ly_giong.py thu-am.m4a --cat-lang      # rút ngắn các khoảng im lặng quá 1,2 giây

Chỉ cần ffmpeg. File ra dùng thẳng cho:  dung_video.py --giong thu-am-dep.wav
"""
import argparse
import subprocess
import sys
from pathlib import Path

KIEU = {
    #        dày (160Hz)  đục (350Hz)  rõ chữ (3.5kHz)  thoáng (9kHz)
    "am":   dict(day=3.0, duc=-2.5, ro=2.0, thoang=1.0),
    "sang": dict(day=1.5, duc=-3.0, ro=3.5, thoang=2.5),
    "nhe":  dict(day=1.5, duc=-1.5, ro=1.0, thoang=0.5),
}


def chuoi_loc(k, khu_on, cat_lang):
    f = [
        "aresample=48000",
        "highpass=f=75",                                   # bỏ ù trầm, tiếng chạm bàn
        f"afftdn=nr={khu_on}:nf=-45:tn=1",                 # khử ồn nền (quạt, điều hoà)
        f"equalizer=f=160:t=o:w=1.2:g={k['day']}",         # độ dày, "nội lực"
        f"equalizer=f=350:t=o:w=1.0:g={k['duc']}",         # bớt đục, bớt "giọng trong hộp"
        f"equalizer=f=3500:t=o:w=1.4:g={k['ro']}",         # rõ chữ
        f"equalizer=f=9000:t=o:w=1.5:g={k['thoang']}",     # thoáng
        "deesser=i=0.4:m=0.5:f=0.5",                       # bớt tiếng xì (s, x)
        "acompressor=threshold=-22dB:ratio=3.5:attack=8:release=160:makeup=4dB:knee=6dB",  # giọng đều, chắc
        "acompressor=threshold=-12dB:ratio=2:attack=20:release=250",                       # nén nhẹ lần 2
    ]
    if cat_lang:
        f.append("silenceremove=stop_periods=-1:stop_duration=1.2:stop_threshold=-42dB:stop_silence=0.7")
    f += ["loudnorm=I=-16:TP=-1.5:LRA=8", "alimiter=limit=0.84"]
    return ",".join(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vao", type=Path)
    ap.add_argument("--kieu", choices=list(KIEU), default="am")
    ap.add_argument("--khu-on", type=int, default=10, help="mức khử ồn 0–30 dB")
    ap.add_argument("--cat-lang", action="store_true")
    ap.add_argument("--ra", type=Path)
    a = ap.parse_args()
    ra = a.ra or a.vao.with_name(a.vao.stem + "-dep.wav")
    loc = chuoi_loc(KIEU[a.kieu], a.khu_on, a.cat_lang)
    for dich, them in ((ra, ["-c:a", "pcm_s16le"]), (ra.with_suffix(".mp3"), ["-b:a", "192k"])):
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(a.vao), "-vn", "-ac", "1",
                            "-af", loc, "-ar", "48000", *them, str(dich)])
        if r.returncode:
            sys.exit("Lỗi xử lý âm thanh")
    print(f"✔ {ra}  (+ {ra.with_suffix('.mp3').name})  kiểu={a.kieu}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Máy dựng video tự động: KỊCH BẢN -> GIỌNG ĐỌC -> GHÉP CẢNH NỀN -> NHẠC -> PHỤ ĐỀ -> MP4.

Ý tưởng: hình chỉ là "cảnh tay người đang làm gì đó" (nấu ăn, pha trà, viết thư pháp,
làm gốm...), âm thanh là câu chuyện. Mỗi lần dựng, máy cắt các clip nguồn ở vị trí
ngẫu nhiên, độ dài ngẫu nhiên, đảo thứ tự, lật ngang, zoom nhẹ -> cùng một kho clip
nhưng KHÔNG video nào có kết cấu giống hệt video nào (đổi --seed là ra bản khác).

Cách dùng (chạy trên máy anh/chị, cần internet cho giọng đọc):
  pip install edge-tts
  python dung_video.py --kich-ban ../kenh-1-chuyen-doi/kich-ban-goc/001-*.md \
      --clips ../assets/clips/nau-an --nhac ../assets/nhac/tu-tao \
      --khung 16x9 --ra ../xuat/001.mp4

  # Bản TikTok/Shorts dọc 9:16, dùng phần "BẢN NGẮN" trong kịch bản:
  python dung_video.py --kich-ban ... --phan ngan --khung 9x16 --ra ../xuat/001-short.mp4

  # Đã có file giọng thu sẵn (giọng thật hoặc từ app khác) thì bỏ qua bước TTS:
  python dung_video.py --giong giong.mp3 --clips ... --ra ...

Kịch bản: văn bản đọc nằm giữa 2 dòng
  <!-- DOC -->   ...   <!-- HET DOC -->        (bản dài)
  <!-- DOC NGAN --> ... <!-- HET DOC NGAN -->  (bản ngắn)
"""
import argparse
import asyncio
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GIONG_MAC_DINH = "vi-VN-NamMinhNeural"  # giọng nam trầm; giọng nữ: vi-VN-HoaiMyNeural
DUOI_VIDEO = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
KHUNG = {"16x9": (1920, 1080), "9x16": (1080, 1920), "1x1": (1080, 1080)}


def chay(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"Lỗi khi chạy: {' '.join(cmd[:6])} ...")
    return r.stdout


def do_dai(path):
    out = chay(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "json", str(path)])
    return float(json.loads(out)["format"]["duration"])


def lay_van_ban(kich_ban: Path, phan: str) -> str:
    raw = kich_ban.read_text(encoding="utf-8")
    mo, dong = ("<!-- DOC NGAN -->", "<!-- HET DOC NGAN -->") if phan == "ngan" \
        else ("<!-- DOC -->", "<!-- HET DOC -->")
    m = re.search(re.escape(mo) + r"(.*?)" + re.escape(dong), raw, re.S)
    if not m:
        raise SystemExit(f"Không thấy đoạn {mo} ... {dong} trong {kich_ban}")
    txt = m.group(1)
    txt = re.sub(r"\[ngừng[^\]]*\]", "\n…\n", txt)  # [ngừng 2s] -> khoảng lặng
    txt = re.sub(r"\[.*?\]", "", txt)          # bỏ các ghi chú đạo diễn khác
    txt = re.sub(r"[*_#>`]", "", txt)          # bỏ ký hiệu markdown
    txt = re.sub(r"\n{2,}", "\n\n", txt).strip()
    return txt


async def _tts(text, voice, rate, pitch, mp3, srt):
    import edge_tts
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=proxy)
    sub = edge_tts.SubMaker()
    with open(mp3, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub.feed(chunk)
    Path(srt).write_text(sub.get_srt(), encoding="utf-8")


def tao_giong(text, voice, rate, pitch, thu_muc):
    mp3, srt = thu_muc / "giong.mp3", thu_muc / "phude.srt"
    asyncio.run(_tts(text, voice, rate, pitch, mp3, srt))
    return mp3, srt


def danh_sach_clip(thu_muc):
    clips = sorted(p for p in Path(thu_muc).rglob("*") if p.suffix.lower() in DUOI_VIDEO)
    if not clips:
        raise SystemExit(f"Không có clip nào trong {thu_muc}")
    return [(p, do_dai(p)) for p in clips]


def len_lich_cat(clips, tong, rng, min_s=4.0, max_s=9.0):
    """Xếp các đoạn cắt: không lặp lại clip liền kề, vị trí cắt ngẫu nhiên."""
    lich, t, truoc = [], 0.0, None
    while t < tong:
        ung_vien = [c for c in clips if c[0] != truoc] or clips
        path, dur = rng.choice(ung_vien)
        dai = min(rng.uniform(min_s, max_s), max(dur - 0.2, 0.5))
        bat_dau = rng.uniform(0, max(dur - dai - 0.1, 0))
        lich.append({"clip": path, "tu": round(bat_dau, 2), "dai": round(dai, 2),
                     "lat": rng.random() < 0.35, "zoom": round(rng.uniform(1.0, 1.12), 3),
                     "sang": round(rng.uniform(-0.04, 0.04), 3)})
        t += dai
        truoc = path
    return lich


def cat_doan(d, w, h, fps, out):
    vf = [f"scale={int(w*d['zoom'])}:{int(h*d['zoom'])}:force_original_aspect_ratio=increase",
          f"crop={w}:{h}", f"eq=brightness={d['sang']}", f"fps={fps}", "setsar=1",
          "format=yuv420p"]
    if d["lat"]:
        vf.insert(2, "hflip")
    chay(["ffmpeg", "-y", "-v", "error", "-ss", str(d["tu"]), "-t", str(d["dai"]),
          "-i", str(d["clip"]), "-an", "-vf", ",".join(vf),
          "-c:v", "libx264", "-preset", "fast", "-crf", "25", str(out)])


DUOI_NHAC = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}


def lam_nen_nhac(nguon, tong, rng, muc, giu_goc, tmp):
    """Xử lý từng bản nhạc cho dịu và đều, xáo thứ tự, nối nhau cho đủ dài."""
    ds = []
    for p in nguon:
        p = Path(p)
        ds += sorted(x for x in p.rglob("*") if x.suffix.lower() in DUOI_NHAC) if p.is_dir() else [p]
    if not ds:
        raise SystemExit("Không thấy file nhạc nào")
    rng.shuffle(ds)
    diu = "" if giu_goc else "lowpass=f=5000,acompressor=threshold=-24dB:ratio=3:attack=50:release=600,"
    xong, t, i = [], 0.0, 0
    while t < tong + 5:
        src = ds[i % len(ds)]
        out = tmp / f"nhac{i % len(ds):02d}.wav"
        if not out.exists():
            d = do_dai(src)
            chay(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", "48000", "-af",
                  f"{diu}loudnorm=I={muc}:TP=-6:LRA=5,afade=t=in:d=2,afade=t=out:st={max(d-3,0):.2f}:d=3",
                  str(out)])
        xong.append(out)
        t += do_dai(out)
        i += 1
    lst = tmp / "nhac.txt"
    lst.write_text("".join(f"file '{x}'\n" for x in xong))
    bed = tmp / "nen_nhac.wav"
    chay(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bed)])
    print("• Nhạc nền:", " → ".join(x.stem for x in ds[:min(len(ds), i)]))
    return bed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kich-ban", type=Path, help="file kịch bản .md")
    ap.add_argument("--phan", choices=["dai", "ngan"], default="dai")
    ap.add_argument("--giong", type=Path, help="file giọng có sẵn (bỏ qua TTS)")
    ap.add_argument("--phu-de", type=Path, help="file .srt có sẵn (khi dùng --giong)")
    ap.add_argument("--may", choices=["edge", "vieneu"], default="edge",
                    help="máy đọc: edge (Microsoft, cần mạng) hoặc vieneu (chạy tại máy, tự nhiên hơn)")
    ap.add_argument("--voice", default=None, help="tên giọng; vieneu vd 'Ngọc Linh', edge vd vi-VN-NamMinhNeural")
    ap.add_argument("--toc-do-vieneu", type=float, default=1.0)
    ap.add_argument("--toc-do", default="-5%", help="tốc độ đọc, vd -10%%, +0%%")
    ap.add_argument("--cao-do", default="-2Hz")
    ap.add_argument("--clips", type=Path, required=True, help="thư mục clip nền")
    ap.add_argument("--nhac", type=Path, nargs="+",
                    help="một hay nhiều file nhạc / thư mục nhạc; nhiều bản thì xáo thứ tự theo seed và nối nhau")
    ap.add_argument("--muc-nhac", type=float, default=-30,
                    help="độ to của nhạc nền (LUFS). Giọng ở -16; -30 là nhạc rất nhẹ, -26 rõ hơn")
    ap.add_argument("--nhac-goc", action="store_true",
                    help="giữ nguyên âm sắc nhạc (mặc định: cắt bớt âm cao + nén cho dịu, dễ nghe ban đêm)")
    ap.add_argument("--khung", choices=list(KHUNG), default="16x9")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--khong-phu-de", action="store_true", help="không in phụ đề lên hình")
    ap.add_argument("--seed", type=int, help="đổi seed = đổi kết cấu ghép")
    ap.add_argument("--ra", type=Path, required=True)
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit("Cần cài ffmpeg trước: https://ffmpeg.org/download.html")

    seed = a.seed if a.seed is not None else random.randrange(10**6)
    rng = random.Random(seed)
    w, h = KHUNG[a.khung]
    tmp = Path(tempfile.mkdtemp(prefix="dung_"))

    # 1) Giọng đọc + phụ đề
    if a.giong:
        giong, srt = a.giong, a.phu_de
    else:
        if not a.kich_ban:
            raise SystemExit("Cần --kich-ban hoặc --giong")
        text = lay_van_ban(a.kich_ban, a.phan)
        if a.may == "vieneu":
            import giong_vieneu
            a.voice = a.voice or "Ngọc Linh"
            print(f"• Đọc {len(text.split())} chữ bằng VieNeu, giọng {a.voice} ...")
            giong, srt = tmp / "giong.wav", tmp / "phude.srt"
            giong_vieneu.doc(text, a.voice, giong, srt, a.toc_do_vieneu)
        else:
            a.voice = a.voice or GIONG_MAC_DINH
            print(f"• Đọc {len(text.split())} chữ bằng giọng {a.voice} ...")
            giong, srt = tao_giong(text, a.voice, a.toc_do, a.cao_do, tmp)
    tong = do_dai(giong)
    print(f"• Giọng dài {tong/60:.1f} phút")

    # 2) Cắt & ghép cảnh nền
    clips = danh_sach_clip(a.clips)
    lich = len_lich_cat(clips, tong + 1, rng)
    print(f"• Ghép {len(lich)} đoạn từ {len(clips)} clip (seed={seed})")
    ds = tmp / "ds.txt"
    with open(ds, "w") as f:
        for i, d in enumerate(lich):
            out = tmp / f"d{i:04d}.mp4"
            cat_doan(d, w, h, a.fps, out)
            f.write(f"file '{out}'\n")
    nen = tmp / "nen.mp4"
    chay(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(ds),
          "-c", "copy", str(nen)])

    # 3) Trộn giọng + nhạc, in phụ đề
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(nen), "-i", str(giong)]
    if a.nhac:
        nen_nhac = lam_nen_nhac(a.nhac, tong, rng, a.muc_nhac, a.nhac_goc, tmp)
        cmd += ["-i", str(nen_nhac)]
        af = (f"[2:a]afade=t=in:d=3,afade=t=out:st={max(tong-5,0)}:d=5[n];"
              f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[g];"
              f"[g][n]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
              f"alimiter=limit=0.84[a]")
    else:
        af = "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    vf = "[0:v]null[v]"
    if srt and Path(srt).exists() and not a.khong_phu_de:
        co = 16 if a.khung == "16x9" else 10
        le = 22 if a.khung == "16x9" else 70
        style = (f"FontName=Be Vietnam Pro,FontSize={co},PrimaryColour=&H00FFFFFF,"
                 f"OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=0,"
                 f"MarginV={le},Alignment=2")
        srt_safe = str(Path(srt).resolve()).replace("\\", "/").replace(":", r"\:")
        vf = f"[0:v]subtitles='{srt_safe}':force_style='{style}'[v]"
    cmd += ["-filter_complex", f"{vf};{af}", "-map", "[v]", "-map", "[a]",
            "-t", f"{tong:.2f}", "-c:v", "libx264", "-preset", "fast", "-crf", "25",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(a.ra)]
    a.ra.parent.mkdir(parents=True, exist_ok=True)
    chay(cmd)
    if srt and Path(srt).exists():
        shutil.copy(srt, a.ra.with_suffix(".srt"))   # để upload phụ đề riêng lên YouTube
    (a.ra.with_suffix(".lich-cat.json")).write_text(
        json.dumps({"seed": seed, "doan": [{**d, "clip": str(d["clip"])} for d in lich]},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"✔ Xong: {a.ra}")


if __name__ == "__main__":
    main()

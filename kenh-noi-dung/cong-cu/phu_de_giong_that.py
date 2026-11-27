#!/usr/bin/env python3
"""
Làm phụ đề .srt cho GIỌNG THU THẬT: máy nghe file thu để lấy mốc thời gian từng chữ,
rồi khớp với lời trong kịch bản -> phụ đề đúng chính tả theo kịch bản, đúng nhịp theo giọng đọc.
Đọc lệch kịch bản vài chữ, đọc lại một câu... vẫn khớp được.

  pip install faster-whisper
  python phu_de_giong_that.py --giong thu-dep.wav --kich-ban ../podcast/001-*.md --ra thu-dep.srt
  # không có kịch bản thì bỏ --kich-ban: phụ đề lấy thẳng từ lời máy nghe được (cần soát chính tả)
"""
import argparse
import difflib
import re
import unicodedata
from pathlib import Path


def chuan(w):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w).lower())


def tg(t):
    ms = int(round(max(t, 0) * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def nghe(giong, co="small"):
    from faster_whisper import WhisperModel
    m = WhisperModel(co, device="cpu", compute_type="int8")
    import subprocess
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(giong), "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], stdout=subprocess.PIPE, check=True).stdout
    am = np.frombuffer(raw, dtype=np.float32)
    segs, _ = m.transcribe(am, language="vi", word_timestamps=True, vad_filter=True)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or []) if w.word.strip()]


def manh_phu_de(text, toi_da=62):
    out = []
    for cau in re.findall(r"[^.!?…\n]+[.!?…]*[\"”')]*", text):
        cau = cau.strip()
        if not re.search(r"\w", cau):
            continue
        cur = ""
        for p in re.split(r"(?<=[,;:])\s+", cau):
            if cur and len(cur) + len(p) + 1 > toi_da:
                out.append(cur)
                cur = p
            else:
                cur = (cur + " " + p).strip()
        if cur:
            out.append(cur)
    return out


def khop(tu_nghe, manh):
    a = [chuan(w) for w, _, _ in tu_nghe]
    b, chu = [], []                       # b: từ kịch bản; chu[i] = chỉ số mảnh
    for i, m in enumerate(manh):
        for w in m.split():
            if chuan(w):
                b.append(chuan(w))
                chu.append(i)
    moc = [None] * len(b)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            moc[blk.b + k] = (tu_nghe[blk.a + k][1], tu_nghe[blk.a + k][2])
    kq = []
    for i, m in enumerate(manh):
        ts = [moc[j] for j in range(len(b)) if chu[j] == i and moc[j]]
        tong = sum(1 for j in range(len(b)) if chu[j] == i)
        if ts and len(ts) >= max(1, tong * 0.4):      # mảnh nào khớp quá ít coi như không được đọc
            kq.append([ts[0][0], ts[-1][1], m])
    for i in range(len(kq) - 1):                      # không chồng nhau, giữ chữ thêm một nhịp
        kq[i][1] = min(max(kq[i][1] + 0.25, kq[i][0] + 0.8), kq[i + 1][0] - 0.02)
    return kq, len(manh) - len(kq)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--giong", type=Path, required=True)
    ap.add_argument("--kich-ban", type=Path)
    ap.add_argument("--phan", choices=["dai", "ngan"], default="dai")
    ap.add_argument("--co", default="small", help="cỡ mô hình nghe: small (nhanh) / medium (chuẩn hơn, chậm)")
    ap.add_argument("--ra", type=Path)
    a = ap.parse_args()
    ra = a.ra or a.giong.with_suffix(".srt")
    tu = nghe(a.giong, a.co)
    if a.kich_ban:
        from dung_video import lay_van_ban
        text = lay_van_ban(a.kich_ban, a.phan).replace("…", " ")
        kq, bo = khop(tu, manh_phu_de(text))
        print(f"• Khớp {len(kq)} dòng phụ đề với kịch bản, {bo} dòng không thấy trong file thu")
    else:
        kq, cur = [], []
        for w, s, e in tu:
            cur.append((w, s, e))
            if len(" ".join(x[0] for x in cur)) > 55 or w[-1:] in ".?!":
                kq.append([cur[0][1], cur[-1][2], " ".join(x[0] for x in cur)])
                cur = []
        if cur:
            kq.append([cur[0][1], cur[-1][2], " ".join(x[0] for x in cur)])
    ra.write_text("".join(f"{i}\n{tg(s)} --> {tg(e)}\n{m}\n\n" for i, (s, e, m) in enumerate(kq, 1)),
                  encoding="utf-8")
    print(f"✔ {ra}")


if __name__ == "__main__":
    main()

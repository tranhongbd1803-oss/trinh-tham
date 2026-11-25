#!/usr/bin/env python3
"""
Tạo giọng đọc bằng VieNeu-TTS (mã nguồn mở, chạy ngay trên máy, không cần khoá API).
Đọc từng câu, chèn khoảng lặng thật giữa câu / đoạn / chỗ "…", và tự sinh phụ đề .srt.

  pip install vieneu
  python giong_vieneu.py --van-ban loi.txt --giong "Ngọc Linh" --ra giong.wav
  python giong_vieneu.py --liet-ke          # xem danh sách giọng

dung_video.py gọi module này khi chạy với  --may vieneu
"""
import argparse
import os
import re
from pathlib import Path

import numpy as np

LANG_CAU, LANG_DOAN, LANG_NGUNG = 0.28, 0.65, 1.3   # giây


def tach(text):
    """-> list ('cau', str) | ('lang', giây)."""
    out = []
    for doan in re.split(r"\n\s*\n", text.strip()):
        doan = doan.strip()
        if not doan:
            continue
        if doan == "…":
            out.append(("lang", LANG_NGUNG))
            continue
        for dong in doan.split("\n"):
            for cau in re.findall(r"[^.!?…]+[.!?…]+[\"”')]*|[^.!?…]+$", dong.strip()):
                cau = cau.strip()
                if re.search(r"\w", cau):
                    out += [("cau", cau), ("lang", LANG_CAU)]
        if out and out[-1][0] == "lang":
            out[-1] = ("lang", LANG_DOAN)
    return out


def _tg(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


def _chia_phu_de(cau, toi_da=62):
    """Câu dài -> vài dòng phụ đề, ngắt ở dấu phẩy."""
    if len(cau) <= toi_da:
        return [cau]
    manh, cur = [], ""
    for p in re.split(r"(?<=[,;:])\s+", cau):
        if cur and len(cur) + len(p) + 1 > toi_da:
            manh.append(cur)
            cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        manh.append(cur)
    return manh


def doc(text, giong, wav, srt, toc_do=1.0, tts=None, bao=print):
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    from vieneu import Vieneu
    tts = tts or Vieneu()
    sr = tts.sample_rate
    khuc, phu_de, t = [], [], 0.0
    muc = tach(text)
    n_cau = sum(1 for k, _ in muc if k == "cau")
    i = 0
    for kieu, v in muc:
        if kieu == "lang":
            khuc.append(np.zeros(int(sr * v), dtype=np.float32))
            t += v
            continue
        i += 1
        kw = {"voice": giong}
        if abs(toc_do - 1.0) > 0.01:
            kw["speed"] = toc_do
        try:
            a = tts.infer(v, **kw)
        except TypeError:
            kw.pop("speed", None)
            a = tts.infer(v, **kw)
        a = np.asarray(a, dtype=np.float32).reshape(-1)
        dai = len(a) / sr
        manh = _chia_phu_de(v)
        tong = sum(len(m) for m in manh)
        t0 = t
        for m in manh:
            d = dai * len(m) / tong
            phu_de.append((t0, t0 + d, m))
            t0 += d
        khuc.append(a)
        t += dai
        if i % 10 == 0:
            bao(f"  … {i}/{n_cau} câu")
    am = np.concatenate(khuc) if khuc else np.zeros(1, dtype=np.float32)
    tts.save(am, str(wav))
    Path(srt).write_text("".join(f"{k}\n{_tg(a)} --> {_tg(b)}\n{m}\n\n"
                                 for k, (a, b, m) in enumerate(phu_de, 1)), encoding="utf-8")
    return tts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--van-ban", type=Path)
    ap.add_argument("--giong", default="Ngọc Linh")
    ap.add_argument("--toc-do", type=float, default=1.0)
    ap.add_argument("--ra", type=Path, default=Path("giong.wav"))
    ap.add_argument("--liet-ke", action="store_true")
    a = ap.parse_args()
    if a.liet_ke:
        from vieneu import Vieneu
        for nhan, _ in Vieneu().list_preset_voices():
            print(nhan)
    else:
        doc(a.van_ban.read_text(encoding="utf-8"), a.giong, a.ra, a.ra.with_suffix(".srt"), a.toc_do)
        print("✔", a.ra)

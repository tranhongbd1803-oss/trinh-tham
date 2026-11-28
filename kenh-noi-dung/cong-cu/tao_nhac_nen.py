#!/usr/bin/env python3
"""
Tự tạo nhạc nền tĩnh bằng máy (tổng hợp âm thanh từ số 0) — không lấy từ kho nhạc nào,
nên không ai có thể nhận quyền (Content ID) trên YouTube.

  python tao_nhac_nen.py --ra ../assets/nhac/tu-tao            # tạo cả 3 bản, mỗi bản 4 phút
  python tao_nhac_nen.py --kieu chuong --phut 6 --seed 7 --ra thu-muc

Kiểu:  am     — hợp âm trầm ấm chuyển chậm
       mo     — tiếng nền mở, lơ lửng, gần như đứng yên
       chuong — nền trầm + tiếng chuông nhỏ thưa (kiểu đàn đá / chuông gió)
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np

SR = 44100
NOTE = {n: 440 * 2 ** ((i - 9) / 12) for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def f(ten):                      # "D3" -> Hz
    return NOTE[ten[:-1]] * 2 ** (int(ten[-1]) - 4)


def pad(freq, dai, rng, sang=0.25):
    """Một nốt nền: 3 sóng sin lệch tần nhẹ + chút hoạ âm, to nhỏ thở chậm."""
    t = np.arange(int(dai * SR)) / SR
    out = np.zeros((len(t), 2))
    for det, pan in ((-0.25, 0.3), (0.0, 0.5), (0.3, 0.7)):
        fr = freq * (1 + det / 100)
        ph = rng.uniform(0, 2 * np.pi)
        s = np.sin(2 * np.pi * fr * t + ph) + sang * np.sin(2 * np.pi * 2 * fr * t + ph * 1.3) / 2 \
            + sang * np.sin(2 * np.pi * 3 * fr * t + ph * 0.7) / 5
        s *= 0.75 + 0.25 * np.sin(2 * np.pi * rng.uniform(0.03, 0.09) * t + rng.uniform(0, 6))
        out[:, 0] += s * (1 - pan)
        out[:, 1] += s * pan
    return out / 3


def bao(n, len_, xuong):
    e = np.ones(n)
    a, r = int(len_ * SR), int(xuong * SR)
    e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    e[-r:] = np.cos(np.linspace(0, np.pi / 2, r)) ** 2
    return e[:, None]


def chuong(freq, rng):
    dai = 6.0
    t = np.arange(int(dai * SR)) / SR
    s = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.01 * t) * np.exp(-t * 1.5)
         + 0.12 * np.sin(2 * np.pi * freq * 3.02 * t) * np.exp(-t * 3)) * np.exp(-t * 0.9)
    s[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    pan = rng.uniform(0.25, 0.75)
    return np.stack([s * (1 - pan), s * pan], axis=1)


KIEU = {
    "am": dict(hop_am=[["D2", "A2", "F#3", "E4"], ["B1", "F#2", "D3", "A3"], ["G1", "D3", "B3", "A3"], ["A1", "E3", "C#4", "B3"]], nhip=18, sang=0.22),
    "mo": dict(hop_am=[["C2", "G2", "D3", "G3"], ["C2", "G2", "E3", "A3"], ["A1", "E2", "C3", "G3"], ["F1", "C3", "G3", "A3"]], nhip=24, sang=0.12),
    "chuong": dict(hop_am=[["A1", "E2", "A2", "E3"], ["F1", "C2", "A2", "E3"], ["C2", "G2", "C3", "E3"], ["G1", "D2", "B2", "D3"]], nhip=20, sang=0.1,
                   thang=["A4", "C5", "D5", "E5", "G5", "A5", "E4", "G4"]),
}


def tao(kieu, phut, seed):
    k, rng = KIEU[kieu], np.random.default_rng(seed)
    nhip, n_ha = k["nhip"], len(k["hop_am"])
    so = int(np.ceil(phut * 60 / nhip / n_ha)) * n_ha        # tròn vòng hợp âm -> lặp liền mạch
    tong = so * nhip
    N = int(tong * SR)
    mix = np.zeros((N + int(12 * SR), 2))
    cheo = nhip * 0.45
    for i in range(so):
        dai = nhip + cheo
        seg = sum(pad(f(n), dai, rng, k["sang"]) * (1.0 if j == 0 else 0.7) for j, n in enumerate(k["hop_am"][i % n_ha]))
        seg *= bao(len(seg), cheo, cheo)
        a = int(i * nhip * SR)
        mix[a:a + len(seg)] += seg
    if "thang" in k:
        t = 3.0
        while t < tong - 2:
            c = chuong(f(rng.choice(k["thang"])), rng) * rng.uniform(0.10, 0.2)
            a = int(t * SR)
            mix[a:a + len(c)] += c
            t += rng.uniform(4.5, 11)
    mix[:len(mix) - N] += mix[N:]                            # đuôi vòng về đầu
    mix = mix[:N]
    return mix / np.max(np.abs(mix)) * 0.7


def luu(x, path):
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                          "-af", "lowpass=f=4200,aecho=0.8:0.75:90|180|310:0.35|0.25|0.18,"
                                 "aecho=0.8:0.7:520|900:0.25|0.15,highpass=f=40,loudnorm=I=-20:TP=-3:LRA=6",
                          "-b:a", "192k", str(path)], stdin=subprocess.PIPE)
    p.communicate(x.astype(np.float32).tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kieu", choices=list(KIEU) + ["tat-ca"], default="tat-ca")
    ap.add_argument("--phut", type=float, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--ra", type=Path, required=True)
    a = ap.parse_args()
    a.ra.mkdir(parents=True, exist_ok=True)
    for kieu in (KIEU if a.kieu == "tat-ca" else [a.kieu]):
        out = a.ra / f"tu-tao-{kieu}.mp3"
        luu(tao(kieu, a.phut, a.seed), out)
        print("✔", out)

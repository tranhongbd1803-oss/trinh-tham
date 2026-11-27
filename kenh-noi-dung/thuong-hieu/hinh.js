// Logo dạng HÌNH cho kênh Sống Có Gu.
//   node hinh.js            -> bảng so sánh (bang-hinh.png)
//   node hinh.js mat-troi   -> xuất anh-dai-dien.png theo hình đó
const { chromium } = require('playwright');
const rays = (cx, cy, r1, r2, n, c, w) => Array.from({ length: n }, (_, i) => { const a = i * 2 * Math.PI / n;
  return `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy + r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy + r2 * Math.sin(a)}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`; }).join('');
const book = (y, c1, c2, vien) => `<path d="M38 ${y} Q70 ${y - 16} 100 ${y} V${y + 46} Q70 ${y + 30} 38 ${y + 46} Z" fill="${c1}" stroke="${vien}" stroke-width="5" stroke-linejoin="round"/>
  <path d="M162 ${y} Q130 ${y - 16} 100 ${y} V${y + 46} Q130 ${y + 30} 162 ${y + 46} Z" fill="${c2}" stroke="${vien}" stroke-width="5" stroke-linejoin="round"/>`;
const HINH = {
  'mat-troi': { ten: 'A · Mặt trời đeo kính', svg: `
    <defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fe3ff"/><stop offset="1" stop-color="#2f9bff"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#a)"/>
    ${rays(100, 100, 62, 78, 12, '#fff3a8', 8)}
    <circle cx="100" cy="100" r="52" fill="#ffd43b"/>
    <rect x="62" y="82" width="34" height="24" rx="10" fill="#17324d"/><rect x="104" y="82" width="34" height="24" rx="10" fill="#17324d"/>
    <path d="M94 90 H106" stroke="#17324d" stroke-width="5"/><path d="M62 90 L52 84 M138 90 L148 84" stroke="#17324d" stroke-width="5" stroke-linecap="round"/>
    <path d="M70 88 l8 0" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/><path d="M112 88 l8 0" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>
    <path d="M80 120 Q100 138 120 120" fill="none" stroke="#17324d" stroke-width="6" stroke-linecap="round"/>` },
  'sach-nang': { ten: 'B · Mặt trời mọc từ trang sách', svg: `
    <defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe680"/><stop offset="1" stop-color="#ffb347"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#b)"/>
    ${rays(100, 108, 50, 68, 9, '#fff', 7).split('/>').filter((_, i) => i >= 5 || i === 0).join('/>')}
    <circle cx="100" cy="108" r="40" fill="#ff7a59"/>
    <rect x="0" y="118" width="200" height="82" fill="url(#b)"/>
    ${book(112, '#fff', '#fff', '#17324d')}
    <path d="M52 128 Q72 118 90 126 M52 140 Q72 130 90 138 M110 126 Q128 118 148 128 M110 138 Q128 130 148 140" stroke="#17324d" stroke-width="3" fill="none" stroke-linecap="round" opacity=".45"/>` },
  'mam-xanh': { ten: 'C · Mầm xanh trên trang sách', svg: `
    <defs><linearGradient id="c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d7f9a8"/><stop offset="1" stop-color="#5fd38a"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#c)"/>
    <circle cx="150" cy="48" r="20" fill="#ffd43b"/>
    <path d="M100 122 V72" stroke="#12613f" stroke-width="7" stroke-linecap="round"/>
    <path d="M100 92 C70 92 58 72 58 54 C82 54 100 66 100 92 Z" fill="#17a05d"/>
    <path d="M100 80 C128 80 142 62 142 44 C118 44 100 56 100 80 Z" fill="#2fbf71"/>
    ${book(118, '#fff', '#fff', '#12392b')}` },
  'tach-tra': { ten: 'D · Tách trà và cuốn sách', svg: `
    <defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc2b3"/><stop offset="1" stop-color="#ff6f91"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#d)"/>
    <path d="M78 44 q-10 12 0 22 q10 10 0 22 M104 38 q-10 12 0 22 q10 10 0 22" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".9"/>
    <path d="M132 104 h10 a16 16 0 0 1 0 32 h-14" fill="none" stroke="#fff" stroke-width="9"/>
    <path d="M50 98 H134 V126 A30 30 0 0 1 104 156 H80 A30 30 0 0 1 50 126 Z" fill="#fff"/>
    <circle cx="80" cy="124" r="5" fill="#4a1230"/><circle cx="106" cy="124" r="5" fill="#4a1230"/>
    <path d="M84 136 Q93 144 102 136" fill="none" stroke="#4a1230" stroke-width="4" stroke-linecap="round"/>
    <rect x="36" y="160" width="128" height="12" rx="6" fill="#4a1230" opacity=".85"/>` },
  'trang-cuoi': { ten: 'E · Cuốn sách mỉm cười', svg: `
    <defs><linearGradient id="e" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cdbbff"/><stop offset="1" stop-color="#7c6cf2"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#e)"/>
    <circle cx="48" cy="48" r="6" fill="#ffd43b"/><circle cx="158" cy="60" r="4" fill="#fff"/><circle cx="150" cy="38" r="3" fill="#ffd43b"/>
    <rect x="54" y="52" width="92" height="106" rx="12" fill="#ffd43b"/>
    <rect x="54" y="52" width="16" height="106" rx="6" fill="#ff9d1c"/>
    <circle cx="96" cy="94" r="6" fill="#24154d"/><circle cx="124" cy="94" r="6" fill="#24154d"/>
    <path d="M92 114 Q110 132 128 114" fill="none" stroke="#24154d" stroke-width="6" stroke-linecap="round"/>
    <path d="M120 52 V34 l10 8 l10 -8 V52 Z" fill="#ff5c8d"/>` },
  'ngoc-lam-nang': { ten: 'F · Nắng lên sau núi', svg: `
    <defs><linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9f3ff"/><stop offset="1" stop-color="#48d1c4"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#f)"/>
    ${rays(100, 112, 50, 66, 14, '#fff7b8', 6)}
    <circle cx="100" cy="112" r="40" fill="#ffd43b"/>
    <path d="M0 150 L52 96 L92 138 L128 104 L200 160 V200 H0 Z" fill="#0f8f8a"/>
    <path d="M0 172 L60 132 L110 164 L150 140 L200 176 V200 H0 Z" fill="#07343d"/>` },
};
(async () => { const b = await chromium.launch(); const chon = process.argv[2];
  if (!chon) {
    const p = await b.newPage({ viewport: { width: 1320, height: 960 } });
    await p.setContent(`<body style="margin:0;background:#fff;font-family:Inter,sans-serif"><div style="display:grid;grid-template-columns:repeat(3,400px);gap:40px;padding:30px 20px">
      ${Object.values(HINH).map(h => `<div><div style="border-radius:50%;overflow:hidden;width:400px;height:400px"><svg viewBox="0 0 200 200" width="400" height="400">${h.svg}</svg></div><div style="text-align:center;font-weight:700;font-size:24px;margin-top:10px;color:#222">${h.ten}</div></div>`).join('')}</div></body>`);
    await p.waitForTimeout(300); await p.screenshot({ path: 'bang-hinh.png' });
  } else {
    const h = HINH[chon]; if (!h) { console.log('Hình:', Object.keys(HINH).join(', ')); process.exit(1); }
    const p = await b.newPage({ viewport: { width: 800, height: 800 } });
    await p.setContent(`<body style="margin:0"><svg viewBox="0 0 200 200" width="800" height="800">${h.svg}</svg></body>`); await p.screenshot({ path: 'anh-dai-dien.png' });
  }
  await b.close(); console.log('ok'); })();

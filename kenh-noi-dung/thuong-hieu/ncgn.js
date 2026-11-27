// Logo + ảnh bìa kênh NÂNG CẤP GÓC NHÌN.
//   node ncgn.js          -> bảng 3 mẫu logo (bang-logo.png)
//   node ncgn.js kinh     -> xuất anh-dai-dien.png + anh-bia-kenh.png theo mẫu đó (kinh | chong-sach | mat)
const { chromium } = require('playwright');
const font = `font-family:'Inter Display','Inter',sans-serif`;
const rays = (cx, cy, r1, r2, n, c, w, a0 = 0, a1 = 2 * Math.PI) => Array.from({ length: n }, (_, i) => { const a = a0 + i * (a1 - a0) / (n - (a1 - a0 < 6 ? 1 : 0));
  return `<line x1="${cx + r1 * Math.cos(a)}" y1="${cy + r1 * Math.sin(a)}" x2="${cx + r2 * Math.cos(a)}" y2="${cy + r2 * Math.sin(a)}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`; }).join('');
const lens = (cx, id) => `<clipPath id="${id}"><circle cx="${cx}" cy="104" r="34"/></clipPath>
  <g clip-path="url(#${id})"><rect x="${cx - 40}" y="60" width="80" height="90" fill="#bfeaff"/>
  ${rays(cx, 118, 22, 31, 7, '#fff', 4, Math.PI, 2 * Math.PI)}
  <circle cx="${cx}" cy="118" r="17" fill="#ffd43b"/><path d="M${cx - 40} 122 Q${cx - 10} 104 ${cx + 40} 124 V150 H${cx - 40} Z" fill="#2fbf71"/></g>
  <circle cx="${cx}" cy="104" r="34" fill="none" stroke="#12284a" stroke-width="8"/>`;
const LOGO = {
  'kinh': { ten: 'A · Cặp kính thấy bình minh', svg: `
    <defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe26b"/><stop offset="1" stop-color="#ffb23e"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#a)"/>
    ${lens(61, 'l1')}${lens(139, 'l2')}
    <path d="M95 100 Q100 94 105 100" fill="none" stroke="#12284a" stroke-width="8" stroke-linecap="round"/>
    <path d="M27 100 L12 92 M173 100 L188 92" stroke="#12284a" stroke-width="8" stroke-linecap="round"/>` },
  'chong-sach': { ten: 'B · Đứng trên sách nhìn xa hơn', svg: `
    <defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9be3ff"/><stop offset="1" stop-color="#4fb4ff"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#b)"/>
    ${rays(140, 70, 30, 42, 12, '#fff6b0', 5)}
    <circle cx="140" cy="70" r="23" fill="#ffd43b"/>
    <rect x="104" y="92" width="96" height="108" fill="#12284a"/>
    <rect x="30" y="150" width="62" height="16" rx="4" fill="#ff7a59"/><rect x="36" y="134" width="54" height="16" rx="4" fill="#fff"/><rect x="28" y="118" width="60" height="16" rx="4" fill="#2fbf71"/>
    <rect x="26" y="166" width="70" height="16" rx="4" fill="#ffd43b"/>
    <circle cx="58" cy="72" r="10" fill="#12284a"/><path d="M50 118 V96 a8 8 0 0 1 16 0 V118 Z" fill="#12284a"/>
    <path d="M64 96 L80 84" stroke="#12284a" stroke-width="6" stroke-linecap="round"/>` },
  'mat': { ten: 'C · Con mắt có mặt trời', svg: `
    <defs><linearGradient id="c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8ff0df"/><stop offset="1" stop-color="#2fc4c9"/></linearGradient></defs>
    <rect width="200" height="200" fill="url(#c)"/>
    <path d="M24 110 Q100 40 176 110 Q100 180 24 110 Z" fill="#fff" stroke="#07343d" stroke-width="8" stroke-linejoin="round"/>
    ${rays(100, 110, 30, 40, 10, '#ffb23e', 5)}
    <circle cx="100" cy="110" r="25" fill="#ffd43b"/><circle cx="100" cy="110" r="10" fill="#07343d"/>
    <path d="M100 52 V26 M88 38 L100 26 L112 38" fill="none" stroke="#07343d" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>` },
};
const bia = (svg) => `<div style="width:2560px;height:1440px;position:relative;overflow:hidden;background:linear-gradient(120deg,#fff1a8 0%,#ffd75a 45%,#ffb85c 100%);${font}">
  <div style="position:absolute;right:-240px;top:-300px;width:1100px;height:1100px;border-radius:50%;background:#fff8d6;opacity:.55"></div>
  <div style="position:absolute;left:-220px;bottom:-460px;width:900px;height:900px;border-radius:50%;background:#7fd7ff;opacity:.35"></div>
  <div style="position:absolute;left:520px;top:520px;width:1520px;height:400px;display:flex;align-items:center;gap:60px">
    <div style="width:300px;height:300px;border-radius:50%;overflow:hidden;flex:none;box-shadow:0 12px 40px rgba(18,40,74,.18)"><svg viewBox="0 0 200 200" width="300" height="300">${svg}</svg></div>
    <div><div style="color:#12284a;font-weight:900;font-size:128px;line-height:1.02;letter-spacing:-.02em">NÂNG CẤP<br>GÓC NHÌN</div>
    <div style="color:#12284a;font-weight:600;font-size:40px;margin-top:22px">Mỗi tuần một cuốn sách, để hiểu mình hơn và là chính mình</div></div>
  </div></div>`;
(async () => { const b = await chromium.launch(); const chon = process.argv[2];
  if (!chon) {
    const p = await b.newPage({ viewport: { width: 1320, height: 490 } });
    await p.setContent(`<body style="margin:0;background:#fff;font-family:Inter,sans-serif"><div style="display:grid;grid-template-columns:repeat(3,400px);gap:40px;padding:30px 20px">
      ${Object.values(LOGO).map(h => `<div><div style="border-radius:50%;overflow:hidden;width:400px;height:400px"><svg viewBox="0 0 200 200" width="400" height="400">${h.svg}</svg></div><div style="text-align:center;font-weight:700;font-size:24px;margin-top:10px;color:#222">${h.ten}</div></div>`).join('')}</div></body>`);
    await p.waitForTimeout(300); await p.screenshot({ path: 'bang-logo.png' });
  } else {
    const h = LOGO[chon]; if (!h) { console.log('Mẫu:', Object.keys(LOGO).join(', ')); process.exit(1); }
    let p = await b.newPage({ viewport: { width: 800, height: 800 } });
    await p.setContent(`<body style="margin:0"><svg viewBox="0 0 200 200" width="800" height="800">${h.svg}</svg></body>`); await p.screenshot({ path: 'anh-dai-dien.png' });
    p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
    await p.setContent(`<body style="margin:0">${bia(h.svg)}</body>`); await p.waitForTimeout(300); await p.screenshot({ path: 'anh-bia-kenh.png' });
  }
  await b.close(); console.log('ok'); })();

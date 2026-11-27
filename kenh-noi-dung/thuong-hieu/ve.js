// Vẽ ảnh đại diện (800x800) và ảnh bìa kênh (2560x1440) cho Trạm Nâng Cấp Tư Duy.  node ve.js
const { chromium } = require('playwright');
const logo = (s) => `<svg viewBox="0 0 200 200" width="${s}" height="${s}"><defs>
<radialGradient id="g" cx="50%" cy="42%" r="60%"><stop offset="0" stop-color="#2a2118"/><stop offset="1" stop-color="#0b0d0e"/></radialGradient>
<radialGradient id="l" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff3c4"/><stop offset=".35" stop-color="#ffb93c"/><stop offset="1" stop-color="#ff9d1c" stop-opacity="0"/></radialGradient></defs>
<rect width="200" height="200" fill="url(#g)"/>
<circle cx="100" cy="78" r="62" fill="url(#l)" opacity=".55"/>
<g fill="none" stroke="#ffab2e" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<path d="M100 132 V78"/><path d="M76 100 L100 76 L124 100"/></g>
<g fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"><path d="M52 150 H148"/><path d="M68 168 H132" opacity=".55"/></g></svg>`;
const font = `font-family:'Inter Display','Inter',sans-serif`;
(async () => { const b = await chromium.launch();
  let p = await b.newPage({ viewport: { width: 800, height: 800 } });
  await p.setContent(`<body style="margin:0">${logo(800)}</body>`); await p.screenshot({ path: 'anh-dai-dien.png' });
  p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
  await p.setContent(`<body style="margin:0"><div style="width:2560px;height:1440px;background:radial-gradient(circle at 50% 45%,#1d2224 0%,#0a0c0d 70%);display:flex;align-items:center;justify-content:center;${font}">
  <div style="width:1500px;display:flex;align-items:center;gap:56px">
    <div style="border-radius:50%;overflow:hidden;width:260px;height:260px;flex:none">${logo(260)}</div>
    <div><div style="color:#fff;font-weight:900;font-size:104px;line-height:1.02;letter-spacing:-.01em">TRẠM <span style="color:#ffab2e">NÂNG CẤP</span><br>TƯ DUY</div>
    <div style="color:#d8d8d8;font-weight:500;font-size:40px;margin-top:22px">Mỗi tuần một cuốn sách, một góc nhìn mới cho những quyết định lớn của bạn</div></div>
  </div></div></body>`); await p.waitForTimeout(300); await p.screenshot({ path: 'anh-bia-kenh.png' });
  await b.close(); console.log('ok'); })();

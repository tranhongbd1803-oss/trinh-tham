// Vẽ ảnh đại diện (800x800) và ảnh bìa kênh (2560x1440) cho kênh Sống Có Gu.  node ve.js
const { chromium } = require('playwright');
const font = `font-family:'Inter Display','Inter',sans-serif`;
const logo = (s) => `<div style="width:${s}px;height:${s}px;position:relative;overflow:hidden;background:linear-gradient(145deg,#ffd84a 0%,#ffb52e 55%,#ff8f5a 100%);${font}">
  <div style="position:absolute;right:${-s*.16}px;top:${-s*.16}px;width:${s*.62}px;height:${s*.62}px;border-radius:50%;background:#fff6c9;opacity:.75"></div>
  <div style="position:absolute;right:${s*.02}px;top:${s*.02}px;width:${s*.28}px;height:${s*.28}px;border-radius:50%;background:#fffdf0"></div>
  <div style="position:absolute;left:0;right:0;top:${s*.30}px;text-align:center;color:#17324d;font-weight:900;line-height:.92;letter-spacing:-.02em">
    <div style="font-size:${s*.15}px;letter-spacing:.02em">SỐNG CÓ</div>
    <div style="font-size:${s*.44}px">GU<span style="color:#fff">.</span></div>
  </div></div>`;
(async () => { const b = await chromium.launch();
  let p = await b.newPage({ viewport: { width: 800, height: 800 } });
  await p.setContent(`<body style="margin:0">${logo(800)}</body>`); await p.waitForTimeout(200); await p.screenshot({ path: 'anh-dai-dien.png' });
  p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
  await p.setContent(`<body style="margin:0"><div style="width:2560px;height:1440px;position:relative;overflow:hidden;background:linear-gradient(120deg,#ffe36b 0%,#ffc23d 45%,#ff9a62 100%);${font}">
  <div style="position:absolute;right:-220px;top:-260px;width:1100px;height:1100px;border-radius:50%;background:#fff6c9;opacity:.6"></div>
  <div style="position:absolute;right:160px;top:120px;width:420px;height:420px;border-radius:50%;background:#fffdf0;opacity:.95"></div>
  <div style="position:absolute;left:-200px;bottom:-420px;width:900px;height:900px;border-radius:50%;background:#ff7f6a;opacity:.25"></div>
  <div style="position:absolute;left:530px;top:535px;width:1500px;height:370px;display:flex;flex-direction:column;justify-content:center">
    <div style="color:#17324d;font-weight:900;font-size:190px;line-height:1;letter-spacing:-.02em">SỐNG CÓ GU<span style="color:#fff">.</span></div>
    <div style="color:#17324d;font-weight:600;font-size:46px;margin-top:26px">Mỗi tuần một cuốn sách, để sống rõ mình hơn và vui hơn</div>
  </div></div></body>`); await p.waitForTimeout(300); await p.screenshot({ path: 'anh-bia-kenh.png' });
  await b.close(); console.log('ok'); })();

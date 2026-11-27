// Vẽ ảnh đại diện (800x800) và ảnh bìa kênh (2560x1440) cho kênh Sống Có Gu.
//   node ve.js            -> bảng so sánh các bộ màu (bang-mau.png)
//   node ve.js xanh-troi  -> xuất anh-dai-dien.png + anh-bia-kenh.png theo bộ màu đó
const { chromium } = require('playwright');
const font = `font-family:'Inter Display','Inter',sans-serif`;
const MAU = {
  'xanh-troi': { ten: '1 · Xanh trời',  nen: 'linear-gradient(145deg,#8fd3ff 0%,#4aa8ff 60%,#3b82f6 100%)', vong: '#dff3ff', tam: '#ffffff', chu: '#0b2a4a', cham: '#ffd43b', phu: '#ffffff' },
  'xanh-la':   { ten: '2 · Xanh lá non', nen: 'linear-gradient(145deg,#c9f27b 0%,#7fd957 55%,#2fbf71 100%)', vong: '#f0ffd0', tam: '#fffff2', chu: '#12392b', cham: '#ffffff', phu: '#ffe14d' },
  'hong-san-ho': { ten: '3 · Hồng san hô', nen: 'linear-gradient(145deg,#ffb3a7 0%,#ff7e8a 55%,#ff5c8d 100%)', vong: '#ffe3dc', tam: '#fff7f2', chu: '#4a1230', cham: '#ffe14d', phu: '#ffffff' },
  'ngoc-lam':  { ten: '4 · Ngọc lam',   nen: 'linear-gradient(145deg,#7ff0e0 0%,#2fd3c6 55%,#12a5b8 100%)', vong: '#d9fff8', tam: '#ffffff', chu: '#07343d', cham: '#ff7a59', phu: '#ffffff' },
  'tim-oai-huong': { ten: '5 · Tím oải hương', nen: 'linear-gradient(145deg,#d6c2ff 0%,#a88bff 55%,#7c6cf2 100%)', vong: '#efe7ff', tam: '#ffffff', chu: '#24154d', cham: '#ffd43b', phu: '#ffffff' },
  'kem-da-sac': { ten: '6 · Kem + đa sắc', nen: 'linear-gradient(145deg,#fffaf0 0%,#fff3d6 100%)', vong: '#ffd43b', tam: '#ff7a59', chu: '#10243d', cham: '#2fbf71', phu: '#4aa8ff' },
};
const logo = (s, m) => `<div style="width:${s}px;height:${s}px;position:relative;overflow:hidden;background:${m.nen};${font}">
  <div style="position:absolute;right:${-s*.16}px;top:${-s*.16}px;width:${s*.62}px;height:${s*.62}px;border-radius:50%;background:${m.vong};opacity:.75"></div>
  <div style="position:absolute;right:${s*.02}px;top:${s*.02}px;width:${s*.28}px;height:${s*.28}px;border-radius:50%;background:${m.tam}"></div>
  <div style="position:absolute;left:0;right:0;top:${s*.30}px;text-align:center;color:${m.chu};font-weight:900;line-height:.92;letter-spacing:-.02em">
    <div style="font-size:${s*.15}px;letter-spacing:.02em">SỐNG CÓ</div>
    <div style="font-size:${s*.44}px">GU<span style="color:${m.cham}">.</span></div>
  </div></div>`;
const bia = (m) => `<div style="width:2560px;height:1440px;position:relative;overflow:hidden;background:${m.nen};${font}">
  <div style="position:absolute;right:-220px;top:-260px;width:1100px;height:1100px;border-radius:50%;background:${m.vong};opacity:.6"></div>
  <div style="position:absolute;right:160px;top:120px;width:420px;height:420px;border-radius:50%;background:${m.tam};opacity:.95"></div>
  <div style="position:absolute;left:-200px;bottom:-420px;width:900px;height:900px;border-radius:50%;background:${m.phu};opacity:.22"></div>
  <div style="position:absolute;left:530px;top:535px;width:1500px;height:370px;display:flex;flex-direction:column;justify-content:center">
    <div style="color:${m.chu};font-weight:900;font-size:190px;line-height:1;letter-spacing:-.02em">SỐNG CÓ GU<span style="color:${m.cham}">.</span></div>
    <div style="color:${m.chu};font-weight:600;font-size:46px;margin-top:26px">Mỗi tuần một cuốn sách, để sống rõ mình hơn và vui hơn</div>
  </div></div>`;
(async () => { const b = await chromium.launch(); const chon = process.argv[2];
  if (!chon) {
    const p = await b.newPage({ viewport: { width: 1320, height: 960 } });
    await p.setContent(`<body style="margin:0;background:#fff;${font}"><div style="display:grid;grid-template-columns:repeat(3,400px);gap:40px 40px;padding:30px 20px">
      ${Object.values(MAU).map(m => `<div><div style="border-radius:50%;overflow:hidden;width:400px;height:400px">${logo(400, m)}</div><div style="text-align:center;font-weight:700;font-size:26px;margin-top:10px;color:#222">${m.ten}</div></div>`).join('')}</div></body>`);
    await p.waitForTimeout(300); await p.screenshot({ path: 'bang-mau.png' });
  } else {
    const m = MAU[chon]; if (!m) { console.log('Bộ màu:', Object.keys(MAU).join(', ')); process.exit(1); }
    let p = await b.newPage({ viewport: { width: 800, height: 800 } });
    await p.setContent(`<body style="margin:0">${logo(800, m)}</body>`); await p.waitForTimeout(200); await p.screenshot({ path: 'anh-dai-dien.png' });
    p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
    await p.setContent(`<body style="margin:0">${bia(m)}</body>`); await p.waitForTimeout(300); await p.screenshot({ path: 'anh-bia-kenh.png' });
  }
  await b.close(); console.log('ok'); })();

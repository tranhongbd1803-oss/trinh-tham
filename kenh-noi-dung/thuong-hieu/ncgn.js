// Logo + ảnh bìa kênh NÂNG CẤP GÓC NHÌN — bản tối giản, chững chạc.
//   node ncgn.js            -> bảng mẫu logo (bang-logo.png)
//   node ncgn.js goc-mo     -> xuất anh-dai-dien.png + anh-bia-kenh.png (goc-mo | goc-mo-xanh | ong-kinh | chu-n)
const { chromium } = require('playwright');
const font = `font-family:'Inter Display','Inter',sans-serif`;
const NAVY = '#0f2440', AMBER = '#f5a623', GIAY = '#fbfaf6', TROI = '#e9f3fb';
const gocMo = (nen, net, cham) => `<rect width="200" height="200" fill="${nen}"/>
  <path d="M150 62 L58 138 L158 138" fill="none" stroke="${net}" stroke-width="15" stroke-linejoin="miter" stroke-linecap="butt"/>
  <circle cx="139" cy="104" r="13" fill="${cham}"/>`;
const LOGO = {
  'goc-mo': { ten: 'A · Góc mở — nền sáng', nen: GIAY, chu: NAVY, svg: gocMo(GIAY, NAVY, AMBER) },
  'goc-mo-xanh': { ten: 'B · Góc mở — nền xanh đậm', nen: NAVY, chu: '#fff', svg: gocMo(NAVY, '#ffffff', AMBER) },
  'ong-kinh': { ten: 'C · Vòng tiêu điểm', nen: GIAY, chu: NAVY, svg: `<rect width="200" height="200" fill="${GIAY}"/>
    <circle cx="100" cy="100" r="52" fill="none" stroke="${NAVY}" stroke-width="13"/>
    <path d="M100 48 A52 52 0 0 1 152 100" fill="none" stroke="${AMBER}" stroke-width="13"/>
    <circle cx="100" cy="100" r="15" fill="${NAVY}"/>` },
  'chu-n': { ten: 'D · Chữ N vươn lên', nen: AMBER, chu: NAVY, svg: `<rect width="200" height="200" fill="${AMBER}"/>
    <path d="M62 146 V58 H80 L122 118 V58 H140 V146 H122 L80 86 V146 Z" fill="${NAVY}"/>
    <path d="M131 30 L152 52 H110 Z" fill="${NAVY}"/>` },
};
const bia = (L) => { const toi = L.nen === NAVY; const nen = toi ? NAVY : (L.nen === AMBER ? '#fbfaf6' : L.nen);
  const chu = toi ? '#fff' : NAVY;
  return `<div style="width:2560px;height:1440px;position:relative;overflow:hidden;background:${nen};${font}">
  <div style="position:absolute;left:0;right:0;top:0;height:18px;background:${AMBER}"></div>
  <div style="position:absolute;left:520px;top:520px;width:1520px;height:400px;display:flex;align-items:center;gap:64px">
    <div style="width:280px;height:280px;flex:none;border-radius:36px;overflow:hidden;${toi ? '' : 'box-shadow:0 0 0 3px rgba(15,36,64,.08)'}"><svg viewBox="0 0 200 200" width="280" height="280">${L.svg}</svg></div>
    <div style="border-left:5px solid ${AMBER};padding-left:56px">
      <div style="color:${chu};font-weight:800;font-size:116px;line-height:1.05;letter-spacing:-.015em">Nâng Cấp Góc Nhìn</div>
      <div style="color:${chu};opacity:.78;font-weight:500;font-size:42px;margin-top:20px">Mỗi tuần một cuốn sách, để hiểu mình hơn và là chính mình</div>
    </div>
  </div></div>`; };
(async () => { const b = await chromium.launch(); const chon = process.argv[2];
  if (!chon) {
    const p = await b.newPage({ viewport: { width: 1320, height: 400 } });
    await p.setContent(`<body style="margin:0;background:#d9dde2;font-family:Inter,sans-serif"><div style="display:grid;grid-template-columns:repeat(4,290px);gap:30px;padding:30px 25px">
      ${Object.values(LOGO).map(h => `<div><div style="border-radius:50%;overflow:hidden;width:290px;height:290px"><svg viewBox="0 0 200 200" width="290" height="290">${h.svg}</svg></div><div style="text-align:center;font-weight:700;font-size:20px;margin-top:12px;color:#222">${h.ten}</div></div>`).join('')}</div></body>`);
    await p.waitForTimeout(300); await p.screenshot({ path: 'bang-logo.png' });
  } else {
    const h = LOGO[chon]; if (!h) { console.log('Mẫu:', Object.keys(LOGO).join(', ')); process.exit(1); }
    let p = await b.newPage({ viewport: { width: 800, height: 800 } });
    await p.setContent(`<body style="margin:0"><svg viewBox="0 0 200 200" width="800" height="800">${h.svg}</svg></body>`); await p.screenshot({ path: 'anh-dai-dien.png' });
    p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
    await p.setContent(`<body style="margin:0">${bia(h)}</body>`); await p.waitForTimeout(300); await p.screenshot({ path: 'anh-bia-kenh.png' });
  }
  await b.close(); console.log('ok'); })();

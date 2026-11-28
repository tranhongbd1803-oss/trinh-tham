#!/usr/bin/env node
/* Khung video TikTok 1080x1920 cho kênh TIỆM VUI VẺ.
   Phần trên trong suốt (video nằm dưới khung), phần dưới là thẻ chữ.

   node khung.js                       -> xuất khung TRỐNG cho mọi bộ màu vào khung/ (dùng trong CapCut, tự gõ chữ)
   node khung.js --mau do-tet --tieu-de "THỊT TRÂU GÁC BẾP|MỒI NHẬU CHUẨN VỊ TẾT" --mo-ta "…" --ra bia.png
                                       -> khung đã có chữ (dấu | là xuống dòng)
   --nen 1  : tô nền đặc (xem thử, không trong suốt)

   Vùng an toàn TikTok: chữ chỉ đặt trong thẻ (y 1215–1625); dưới y 1660 và mép phải 120px bị nút/caption che. */
const { chromium } = require('playwright');
const path = require('path');
const MAU = {
  'bac-ha':  { ten: 'Bạc hà',   nen: ['#e6f7f4', '#cdeee8'], the: ['#bfe6df', '#8fd3c8'], vien: '#ffffff', chu: '#12506b', phu: '#2f6f7d', nhan: '#19a394' },
  'do-tet':  { ten: 'Đỏ Tết',   nen: ['#c8102e', '#8f0d22'], the: ['#fff3d6', '#ffe2a6'], vien: '#ffd166', chu: '#a50e25', phu: '#6b3a12', nhan: '#c8102e' },
  'cam-dao': { ten: 'Cam đào',  nen: ['#fff0e3', '#ffd9bf'], the: ['#ffc9a3', '#ff9f6e'], vien: '#ffffff', chu: '#8a2b0c', phu: '#7a4322', nhan: '#f2692b' },
  'vang-bo': { ten: 'Vàng bơ',  nen: ['#fff8dc', '#ffeeb0'], the: ['#ffe58a', '#ffd04d'], vien: '#ffffff', chu: '#6b4a00', phu: '#73581a', nhan: '#e39a00' },
  'tim-mo':  { ten: 'Tím mơ',   nen: ['#f1ebff', '#ddd0ff'], the: ['#cdbcff', '#a78fff'], vien: '#ffffff', chu: '#34207a', phu: '#4a3a86', nhan: '#6f52e0' },
  'hong-phan': { ten: 'Hồng phấn', nen: ['#ffeaf1', '#ffd0df'], the: ['#ffbdd2', '#ff8fb3'], vien: '#ffffff', chu: '#8a1846', phu: '#7d3554', nhan: '#e83e7c' },
};
const a = {}; process.argv.slice(2).forEach((v, i, arr) => { if (v.startsWith('--')) a[v.slice(2)] = arr[i + 1]; });
const esc = s => String(s || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const hexa = (h, o) => { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${o})`; };

function html(m, tieuDe, moTa, nenDac) {
  const sao = [[92, 1178, 18], [1004, 1196, 14], [150, 1700, 16], [930, 1722, 22], [540, 1760, 12], [760, 1690, 10], [330, 1745, 9]]
    .map(([x, y, r]) => `<path transform="translate(${x} ${y}) scale(${r / 10})" d="M0-10 L2.2-2.2 10 0 2.2 2.2 0 10 -2.2 2.2 -10 0 -2.2-2.2Z" fill="${m.vien}" opacity=".85"/>`).join('');
  return `<html><body style="margin:0;background:${nenDac ? '#555' : 'transparent'}">
<div style="width:1080px;height:1920px;position:relative;overflow:hidden;font-family:'Inter Display','Inter',sans-serif">
  <!-- nền dưới: mờ dần từ trong suốt sang màu -->
  <div style="position:absolute;left:0;right:0;top:980px;height:240px;background:linear-gradient(180deg,${hexa(m.nen[0], 0)} 0%,${hexa(m.nen[0], .75)} 55%,${m.nen[0]} 100%)"></div>
  <div style="position:absolute;left:0;right:0;top:1219px;bottom:0;background:linear-gradient(180deg,${m.nen[0]},${m.nen[1]})"></div>
  <svg width="1080" height="1920" style="position:absolute;inset:0">${sao}</svg>
  <!-- lớp thẻ lót -->
  <div style="position:absolute;left:44px;top:1262px;width:992px;height:400px;border-radius:44px;background:${hexa(m.vien, .55)};box-shadow:0 10px 30px ${hexa(m.chu, .12)}"></div>
  <!-- thẻ chính -->
  <div style="position:absolute;left:70px;top:1210px;width:940px;height:420px;border-radius:40px;background:linear-gradient(170deg,${m.the[0]},${m.the[1]});box-shadow:0 14px 34px ${hexa(m.chu, .22)}"></div>
  <div style="position:absolute;left:84px;top:1224px;width:912px;height:392px;border-radius:30px;border:3px dashed ${hexa(m.vien, .9)}"></div>
  <!-- huy hiệu thương hiệu -->
  <div style="position:absolute;left:36px;top:1128px;width:168px;height:168px;border-radius:50%;background:${m.vien};box-shadow:0 8px 22px ${hexa(m.chu, .25)}"></div>
  <svg viewBox="0 0 100 100" width="140" height="140" style="position:absolute;left:50px;top:1142px">
    <circle cx="50" cy="50" r="46" fill="${m.nhan}"/>
    <path d="M30 42 q6 -9 12 0 M58 42 q6 -9 12 0" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
    <path d="M27 56 Q50 84 73 56 Z" fill="#fff"/>
  </svg>
  <!-- tên kênh -->
  <div style="position:absolute;right:86px;top:1176px;background:${m.nhan};color:#fff;font-weight:800;font-size:34px;letter-spacing:.02em;padding:10px 26px;border-radius:999px;box-shadow:0 6px 16px ${hexa(m.chu, .25)}">Tiệm Vui Vẻ</div>
  ${tieuDe ? `<div style="position:absolute;left:120px;top:1262px;width:840px;text-align:center;color:${m.chu};font-weight:900;font-size:${a.co || 62}px;line-height:1.12;letter-spacing:-.01em">${esc(tieuDe).split('|').join('<br>')}</div>` : ''}
  ${moTa ? `<div style="position:absolute;left:124px;top:${a.ymota || 1424}px;width:832px;text-align:center;color:${m.phu};font-weight:500;font-size:${a.comota || 35}px;line-height:1.32">${esc(moTa)}</div>` : ''}
</div></body></html>`;
}
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const chup = async (m, tieuDe, moTa, ra) => { await p.setContent(html(m, tieuDe, moTa, a.nen)); await p.waitForTimeout(250); await p.screenshot({ path: ra, omitBackground: !a.nen }); console.log('✔', ra); };
  if (a.mau) await chup(MAU[a.mau], a['tieu-de'], a['mo-ta'], a.ra || 'khung.png');
  else for (const [k, m] of Object.entries(MAU)) await chup(m, '', '', path.join(__dirname, 'khung', `khung-${k}.png`));
  await b.close();
})();

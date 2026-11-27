#!/usr/bin/env node
/* Làm ảnh bìa YouTube 1280x720 từ một khung hình + chữ lớn.
   node anh_bia.js --nen khung.jpg --to "CÀNG CỐ|CÀNG HỎNG?" --nho "Học cách sống như nước" --nhan "ĐẠO ĐỨC KINH" --mau "#f2c94c" --ra bia.png
   Dấu | trong --to là xuống dòng. */
const { chromium } = require('playwright');
const fs = require('fs');
const a = {}; process.argv.slice(2).forEach((v, i, arr) => { if (v.startsWith('--')) a[v.slice(2)] = arr[i + 1]; });
const esc = s => String(s || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const bg = a.nen ? `url(data:image/jpeg;base64,${fs.readFileSync(a.nen).toString('base64')})` : 'none';
const mau = a.mau || '#f2c94c';
const html = `<html><body style="margin:0"><div style="width:1280px;height:720px;position:relative;overflow:hidden;background:#111;font-family:'Inter Display','Inter',sans-serif">
<div style="position:absolute;inset:0;background:${bg} center/cover;filter:saturate(.9) brightness(.8)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.88) 0%,rgba(0,0,0,.62) 48%,rgba(0,0,0,.05) 100%)"></div>
<div style="position:absolute;left:64px;top:0;bottom:0;width:820px;display:flex;flex-direction:column;justify-content:center;gap:22px">
${a.nhan ? `<div style="align-self:flex-start;background:${mau};color:#111;font-weight:800;font-size:30px;letter-spacing:.06em;padding:8px 18px;border-radius:6px">${esc(a.nhan)}</div>` : ''}
<div style="color:#fff;font-weight:900;font-size:${a.co || 112}px;line-height:1.04;letter-spacing:-.01em;text-shadow:0 4px 24px rgba(0,0,0,.6)">${esc(a.to).split('|').map((l, i) => i % 2 ? `<span style="color:${mau}">${l}</span>` : l).join('<br>')}</div>
${a.nho ? `<div style="color:#fff;font-weight:600;font-size:44px;line-height:1.2;opacity:.95">${esc(a.nho)}</div>` : ''}
</div></div></body></html>`;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.setContent(html); await p.waitForTimeout(300); await p.screenshot({ path: a.ra || 'bia.png' }); await b.close(); console.log('✔', a.ra || 'bia.png'); })();

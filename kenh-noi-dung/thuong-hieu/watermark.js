// Ảnh watermark video 150x150 nền trong suốt.  node watermark.js
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 150, height: 150 }, deviceScaleFactor: 1 });
  await p.setContent(`<body style="margin:0;background:transparent"><svg viewBox="0 0 200 200" width="150" height="150">
  <defs><filter id="s" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity=".45"/></filter></defs>
  <g filter="url(#s)"><path d="M160 46 L40 150 L172 150" fill="none" stroke="#ffffff" stroke-width="20" stroke-linejoin="miter"/>
  <circle cx="146" cy="104" r="18" fill="#f5a623"/></g></svg></body>`);
  await p.screenshot({ path: 'watermark-150.png', omitBackground: true });
  await p.setContent(`<body style="margin:0;background:#444"><img src="file://${process.cwd()}/watermark-150.png" style="position:absolute;right:20px;bottom:20px"><div style="width:400px;height:225px"></div></body>`);
  await p.setViewportSize({ width: 400, height: 225 }); await p.screenshot({ path: '/tmp/claude-0/-home-user-trinh-tham/911fdef4-a0bd-58f8-ac4b-6c0ddb7b597b/scratchpad/wm-xem.png' });
  await b.close(); console.log('ok'); })();

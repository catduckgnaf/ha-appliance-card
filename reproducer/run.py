import asyncio, json, sys, http.server, threading, functools, os
from playwright.async_api import async_playwright
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory='.')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory='.'))
port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
CHECK = """() => [...document.querySelectorAll('appliance-card')].map(c => {
  const r = c.shadowRoot; const cap = c.parentElement.querySelector('.cap').textContent;
  const img = r.querySelector('img.job-icon');
  const app = r.querySelector('img.appliance-img');
  const box = c.getBoundingClientRect(); const lab = r.querySelector('.job-label');
  const lb = lab ? lab.getBoundingClientRect() : null;
  return { scenario: cap, label: lab ? lab.textContent.trim() : null, active: !!r.querySelector('.job-icon-container.active'),
    iconSrcIsData: img ? img.src.startsWith('data:image/png;base64,') : null,
    iconDecoded: img ? (img.complete && img.naturalWidth > 0) : null, iconNatural: img ? [img.naturalWidth,img.naturalHeight] : null,
    applianceDecoded: app ? (app.complete && app.naturalWidth > 0) : null,
    labelRight: lb ? Math.round(lb.right-box.left) : null, labelLeft: lb ? Math.round(lb.left-box.left) : null, imgRight: app ? Math.round(app.getBoundingClientRect().right-box.left) : null, labelInsideCard: lb ? (lb.left >= (app ? app.getBoundingClientRect().right : box.left) + 4 && lb.right <= box.right+0.5) : null,
    cardW: Math.round(box.width), buttons: r.querySelectorAll('button,[role=button]').length };
})"""
async def main():
    out = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        reqs = []
        for name, w, h, theme, cols, extra in [('mobile-dark',390,1500,'dark',1,''),('mobile-light',390,1500,'light',1,''),('desktop-dark',1200,900,'dark',3,''),('desktop-light',1200,900,'light',3,''),('narrow-dark',320,1500,'dark',1,'')]:
            pg = await b.new_page(viewport={'width':w,'height':h}, device_scale_factor=2 if w<500 else 1)
            pg.on('request', lambda r: reqs.append(r.url))
            pg.on('pageerror', lambda e: print('PAGEERROR', e))
            await pg.goto(f'http://127.0.0.1:{port}/harness.html?theme={theme}&cols={cols}&extra=Alert,__missing,__unconfigured,Dispensing%20Hot%20Water,Preparing%20Milk')
            await pg.wait_for_function('window.__ready === true', timeout=30000)
            out[name] = await pg.evaluate(CHECK)
            out[name+'_calls'] = await pg.evaluate('window.__serviceCalls || 0')
            await pg.screenshot(path=f'raw-{name}.png', full_page=True)
            await pg.close()
        await b.close()
    external = sorted({u.split('?')[0] for u in reqs if not u.startswith('data:') and '127.0.0.1' not in u})
    out['non_local_requests'] = external
    out['local_requests'] = sorted({u.split('?')[0].split(str(port))[-1] for u in reqs if '127.0.0.1' in u})
    json.dump(out, open('browser-result.json','w'), indent=1)
    bad = [ (k,r['scenario']) for k,v in out.items() if isinstance(v,list) and k[0] in 'mnd' for r in v if r['iconDecoded'] is False or r['iconSrcIsData'] is False or r['labelInsideCard'] is False]
    print('failures:', bad); print('external:', external); print('local:', out['local_requests'])
    for r in out['desktop-dark']: print(r)
asyncio.run(main())

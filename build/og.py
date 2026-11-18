import asyncio,base64
from playwright.async_api import async_playwright
A='/home/claude/site/dist_assets/'
f=lambda n:base64.b64encode(open(A+n,'rb').read()).decode()
h=f'''<html><style>@font-face{{font-family:I;src:url(data:font/woff2;base64,{f("fonts/inter.woff2")})}}@font-face{{font-family:M;src:url(data:font/woff2;base64,{f("fonts/michroma.woff2")})}}
body{{margin:0;width:1200px;height:630px;background:#0F2A4C;font-family:I;color:#F1EEE7;display:flex;flex-direction:column;justify-content:space-between;padding:72px 80px;box-sizing:border-box;position:relative;overflow:hidden}}
h1{{font-size:58px;line-height:1.05;letter-spacing:-2px;margin:0;font-weight:800;max-width:760px}}
.m{{font-family:M;font-size:18px;letter-spacing:3px;color:#9FB0C4}}
svg{{position:absolute;right:-110px;top:60px;opacity:.9}}</style><body>
<svg width="400" height="490" viewBox="0 0 540 450"><path d="M262 22 L448 82 L448 232 C448 332 368 398 262 428 C156 398 76 332 76 232 L76 82 Z" fill="none" stroke="#16365F" stroke-width="26"/><path d="M128 300 C165 318 192 350 214 386 C282 262 372 150 512 52" fill="none" stroke="#1951E1" stroke-width="32" stroke-linecap="round"/></svg>
<img src="data:image/webp;base64,{f("logo-claro.webp")}" style="width:300px">
<div><div class="m">EMPRÉSTIMO COM GARANTIA DE IMÓVEL · CONSÓRCIO</div><h1 style="margin-top:22px">O banco oferece o que tem na prateleira. A Shield monta o crédito que o seu plano pede.</h1></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':630})
        await pg.set_content(h); await pg.wait_for_timeout(500); await pg.screenshot(path=A+'og.png'); await b.close()
asyncio.run(main())

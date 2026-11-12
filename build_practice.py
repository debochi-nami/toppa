# 練習用（practice/）を本番の index.html から作る。本番を直したら、これを実行し直す。
# 実行： <PYTHON> build_practice.py
import os, re, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, "practice"); os.makedirs(P, exist_ok=True)
rd = lambda f: open(os.path.join(H, f), encoding="utf-8").read()
def wr(f, s): open(os.path.join(P, f), "w", encoding="utf-8", newline="").write(s)
def rep(s, a, b):
    assert s.count(a) == 1, (a, s.count(a)); return s.replace(a, b)
BLUE = "#1565c0"
s = rd("index.html")
s = rep(s, "<title>杭州カラテ突破計算</title>", "<title>杭州カラテ突破計算（練習用）</title>")
s = rep(s, 'name="apple-mobile-web-app-title" content="突破計算"', 'name="apple-mobile-web-app-title" content="突破練習"')
s = rep(s, '<meta name="theme-color" content="#b71c1c">', f'<meta name="theme-color" content="{BLUE}">')
s = rep(s, "<h1>杭州カラテ突破計算（携帯アプリ）</h1>", "<h1>杭州カラテ突破計算（練習用）</h1>")
s = rep(s, '<div class="head">',
        f'<div style="background:{BLUE};color:#fff;border-radius:8px;padding:6px 10px;font-weight:700;font-size:14px">練習用です。本番のアプリ（赤いアイコン）とは入力が別で、ここで入れた結果は本番に入りません。</div><div class="head">')
s = rep(s, 'const LS="wc-hangzhou-v1";', 'const LS="wc-hangzhou-practice-v1";')
wr("index.html", s)
m = json.loads(rd("manifest.webmanifest"))
m.update(name="杭州カラテ突破計算（練習用）", short_name="突破練習", theme_color=BLUE)
wr("manifest.webmanifest", json.dumps(m, ensure_ascii=False, indent=1))
sw = rd("sw.js"); v = re.search(r'const C="toppa-([^"]+)"', sw).group(1)
wr("sw.js", sw.replace(f'toppa-{v}', f'toppa-practice-{v}'))
wr("robots.txt", rd("robots.txt"))
font = next(f for f in [r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc", r"C:\Windows\Fonts\msgothic.ttc"] if os.path.exists(f))
for n in (180, 512):
    im = Image.new("RGB", (n, n), BLUE); d = ImageDraw.Draw(im); f = ImageFont.truetype(font, int(n * 0.36))
    for i, ch in enumerate("練習"):
        d.text((n / 2, n * (0.29 + 0.43 * i)), ch, font=f, fill="white", anchor="mm")
    im.save(os.path.join(P, f"icon-{n}.png"))
print("practice built, cache", f"toppa-practice-{v}")

"""Generates dark + light SVG assets for the GitHub profile README."""
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        fg="#E6EDF3", muted="#8B949E", faint="#30363D", grid="#161B22",
        accent="#818CF8", accent2="#6366F1", live="#3FB950", card="#0D1117", node="#161B22",
    ),
    "light": dict(
        fg="#1F2328", muted="#59636E", faint="#D0D7DE", grid="#F0F2F5",
        accent="#4F46E5", accent2="#6366F1", live="#1A7F37", card="#FFFFFF", node="#F6F8FA",
    ),
}


def style(t):
    return f"""
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .fg {{ fill: {t['fg']}; }}
    .muted {{ fill: {t['muted']}; }}
    .accent {{ fill: {t['accent']}; }}
    .flow {{ stroke-dasharray: 6 10; animation: flow 1.6s linear infinite; }}
    .pulse {{ animation: pulse 1.8s ease-in-out infinite; }}
    .wave {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 3.2s ease-out forwards; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -32; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .flow, .pulse, .wave {{ animation: none; stroke-dashoffset: 0; }}
    }}
  </style>"""


# ---------------------------------------------------------------- header
def header(t):
    W, H = 1200, 340
    grid = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{t["grid"]}" stroke-width="1"/>'
        for x in range(0, W + 1, 40)
    ) + "".join(
        f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{t["grid"]}" stroke-width="1"/>'
        for y in range(0, H + 1, 40)
    )
    # signal trace: flat → burst → flat (reads as "packet / media signal")
    pts, x = [], 600
    import math
    while x <= 1160:
        d = x - 880
        amp = 46 * math.exp(-(d / 110) ** 2)
        y = 170 + amp * math.sin(x / 9.0)
        pts.append(f"{x},{y:.1f}")
        x += 4
    trace = "M" + " L".join(pts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ahmet Demir — Full-Stack &amp; DevOps">{style(t)}
  <defs>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{t['card']}" stop-opacity="1"/>
      <stop offset=".45" stop-color="{t['card']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="tr" x1="0" x2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset=".35" stop-color="{t['accent']}"/>
      <stop offset="1" stop-color="{t['accent2']}"/>
    </linearGradient>
  </defs>
  <g opacity=".9">{grid}</g>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <path d="{trace}" fill="none" stroke="url(#tr)" stroke-width="2" stroke-linecap="round" opacity=".55"/>
  <path d="{trace}" fill="none" stroke="{t['accent']}" stroke-width="2.5" stroke-linecap="round" class="flow"/>
  <line x1="600" y1="170" x2="1160" y2="170" stroke="{t['faint']}" stroke-width="1" stroke-dasharray="2 6"/>

  <g transform="translate(56,0)">
    <circle cx="6" cy="84" r="5" fill="{t['live']}" class="pulse"/>
    <text x="22" y="89" class="mono muted" font-size="15" letter-spacing="2">LIVE · OPITEKYA · TÜRKİYE</text>
    <text x="0" y="168" class="sans fg" font-size="72" font-weight="800" letter-spacing="-2.5">Ahmet Demir</text>
    <text x="2" y="214" class="sans muted" font-size="24" font-weight="500">Full-Stack &amp; DevOps — gerçek zamanlı sistemler, uçtan uca.</text>
    <text x="2" y="268" class="mono accent" font-size="15" letter-spacing=".5">api → signaling → sfu → native gpu → k8s</text>
  </g>
</svg>"""


# ---------------------------------------------------------------- architecture
def node(x, y, w, h, title, sub, t, hl=False):
    stroke = t["accent"] if hl else t["faint"]
    return f"""
  <g transform="translate({x},{y})">
    <rect width="{w}" height="{h}" rx="14" fill="{t['node']}" stroke="{stroke}" stroke-width="{1.5 if hl else 1}"/>
    <text x="20" y="34" class="mono muted" font-size="12" letter-spacing="1.5">{sub}</text>
    <text x="20" y="62" class="sans fg" font-size="20" font-weight="700">{title}</text>
  </g>"""


def edge(path, t, label=None, lx=0, ly=0):
    lab = (f'<text x="{lx}" y="{ly}" class="mono muted" font-size="12" text-anchor="middle">{label}</text>'
           if label else "")
    return f"""
  <path d="{path}" fill="none" stroke="{t['faint']}" stroke-width="2"/>
  <path d="{path}" fill="none" stroke="{t['accent']}" stroke-width="2" class="flow"/>{lab}"""


def architecture(t):
    W, H = 1200, 420
    nw, nh = 210, 84
    X = [40, 343, 646, 949]
    r1, r2 = 70, 270
    c, sg, f, n = (X[0], r1), (X[1], r1), (X[2], r1), (X[3], r1)
    db, k, o = (X[0], r2), (X[1], r2), (X[2], r2)
    mid = lambda a: a[1] + 42
    gap = lambda a: a[0] + nw + 46
    parts = [
        edge(f"M{c[0]+nw},{mid(c)} L{sg[0]},{mid(sg)}", t, "ws", gap(c), r1+30),
        edge(f"M{sg[0]+nw},{mid(sg)} L{f[0]},{mid(f)}", t, "transport", gap(sg), r1+30),
        edge(f"M{n[0]},{mid(n)} L{f[0]+nw},{mid(f)}", t, "rtp", gap(f), r1+30),
        edge(f"M{c[0]+60},{r1+nh} C{c[0]+60},{r1+190} {f[0]+50},{r1+170} {f[0]+50},{r1+nh}", t,
             "webrtc media", 190, 236),
        edge(f"M{sg[0]+150},{r1+nh} L{k[0]+150},{r2}", t),
        edge(f"M{f[0]+160},{r1+nh} L{o[0]+160},{r2}", t),
        edge(f"M{db[0]+nw},{mid(db)} L{k[0]},{mid(k)}", t, "state", gap(db), r2+30),
        edge(f"M{k[0]+nw},{mid(k)} L{o[0]},{mid(o)}", t, "metrics", gap(k), r2+30),
        node(*c, nw, nh, "Web / Desktop", "CLIENT", t),
        node(*sg, nw, nh, "Signaling + API", "NODE 22", t),
        node(*f, nw, nh, "SFU", "MEDIASOUP", t, hl=True),
        node(*n, nw, nh, "GPU Capture", "NATIVE C/C++", t, hl=True),
        node(*db, nw, nh, "Mongo + Redis", "STATE", t),
        node(*k, nw, nh, "Kubernetes", "NGINX · CF", t),
        node(*o, nw, nh, "Observability", "PROM · OTEL", t),
    ]
    legend = f"""
  <g transform="translate({X[3]},{r2+16})">
    <rect width="{nw}" height="52" rx="10" fill="none" stroke="{t['faint']}" stroke-dasharray="3 5"/>
    <circle cx="20" cy="26" r="5" fill="{t['live']}" class="pulse"/>
    <text x="36" y="31" class="mono muted" font-size="13">medya yolu · canlı</text>
  </g>"""
    title = f'<text x="40" y="36" class="mono muted" font-size="13" letter-spacing="2">OPITEKYA · SİSTEM HARİTASI</text>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Opitekya mimarisi: istemci, signaling, mediasoup SFU, native GPU yakalama, Kubernetes, gözlem">{style(t)}
  {title}{''.join(parts)}{legend}
</svg>"""


# ---------------------------------------------------------------- stack
STACK = [
    ("FRONTEND", ["React 19", "TypeScript", "Vite", "Tailwind", "Electron"]),
    ("BACKEND", ["Node 22", "Express", "MongoDB", "Redis", "Socket.IO"]),
    ("REALTIME", ["WebRTC", "mediasoup", "C / C++", "GPU encode"]),
    ("INFRA", ["Kubernetes", "Docker", "Nginx", "Cloudflare", "Linux", "GH Actions"]),
    ("OBSERVE", ["Prometheus", "Grafana", "OpenTelemetry"]),
]


def stack(t):
    W = 1200
    row_h, top = 64, 24
    H = top + row_h * len(STACK) + 8
    out = []
    for i, (cat, items) in enumerate(STACK):
        y = top + i * row_h
        out.append(f'<line x1="0" y1="{y+row_h-6}" x2="{W}" y2="{y+row_h-6}" stroke="{t["faint"]}" stroke-width="1"/>')
        out.append(f'<text x="0" y="{y+30}" class="mono muted" font-size="13" letter-spacing="2">{cat}</text>')
        x = 200
        for it in items:
            w = 40 + len(it) * 9.0
            hl = cat == "REALTIME"
            out.append(
                f'<rect x="{x}" y="{y+6}" width="{w:.0f}" height="36" rx="18" fill="{t["node"]}" '
                f'stroke="{t["accent"] if hl else t["faint"]}"/>'
                f'<text x="{x + w/2:.0f}" y="{y+30}" text-anchor="middle" class="sans fg" font-size="16" font-weight="600">{it}</text>'
            )
            x += w + 12
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Teknoloji yığını">{style(t)}
  {''.join(out)}
</svg>"""


# ---------------------------------------------------------------- footer
def footer(t):
    W, H = 1200, 80
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="footer">{style(t)}
  <line x1="0" y1="20" x2="{W}" y2="20" stroke="{t['faint']}"/>
  <line x1="0" y1="20" x2="{W}" y2="20" stroke="{t['accent']}" stroke-width="2" class="flow"/>
  <circle cx="6" cy="56" r="4" fill="{t['live']}" class="pulse"/>
  <text x="20" y="61" class="mono muted" font-size="13" letter-spacing="1.5">uçtan uca, tek elden — opitekya.com</text>
</svg>"""


for name, fn in [("header", header), ("architecture", architecture), ("stack", stack), ("footer", footer)]:
    for theme, t in THEMES.items():
        (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
print("ok")

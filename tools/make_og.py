#!/usr/bin/env python3
"""生成 1200×630 的 OG 分享图(docs/og.png;--en → docs/og-en.png)。用法:python3 tools/make_og.py [--en]
图:纳斯达克综合指数 2000/2001/2002 三个年度跌幅(−39.3% / −21.1% / −31.5%),峰谷累计 −77.9%、历时 31 个月 —— 数据同正文 §1.1。"""
import sys
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = Path(__file__).resolve().parent.parent
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(FONT)
CJK = fm.FontProperties(fname=FONT)
PAPER, INK, INK2, RULE, GOLD, RED = '#F6F5F2', '#1A1A17', '#63625C', '#DCDAD3', '#8A6D1F', '#B42318'
YEARS = ['2000', '2001', '2002']
DROP = [-39.3, -21.1, -31.5]
EN = '--en' in sys.argv

fig = plt.figure(figsize=(12, 6.3), dpi=100); fig.patch.set_facecolor(PAPER)
if EN:
    fig.text(.065, .80, 'The AI Bubble Against the Dot-com Bubble', fontsize=40, color=INK, weight='bold', family='DejaVu Sans')
    fig.text(.065, .705, 'layered check-up · scenario framework · nine leading indicators', fontsize=21, color=INK2, family='DejaVu Sans')
    fig.text(.065, .175, 'No dates guessed. Layers diagnosed, triggers registered.', fontsize=21, color=GOLD, family='DejaVu Sans')
else:
    fig.text(.065, .80, 'AI 泡沫研究:2000 年互联网泡沫对照', fontproperties=CJK, fontsize=50, color=INK, weight='bold')
    fig.text(.065, .705, '分层体检 · 情景框架 · 九项领先指标仪表盘', fontproperties=CJK, fontsize=25, color=INK2)
    fig.text(.065, .175, '不猜日期。分层识别,判据预注册。', fontproperties=CJK, fontsize=22, color=GOLD)
fig.text(.065, .095, 'ronfi.github.io/ai-bubble', fontsize=19, color=INK2, family='DejaVu Sans')

ax = fig.add_axes([.64, .26, .31, .38]); ax.set_facecolor(PAPER)
ax.bar(YEARS, DROP, color=RED, width=.6)
for x, v in zip(YEARS, DROP):
    ax.text(x, v - 2.5, f'{v:.1f}%', ha='center', va='top', fontsize=13, color=INK, family='DejaVu Sans')
ax.set_ylim(-50, 4); ax.axhline(0, color=RULE, lw=1)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(RULE); ax.tick_params(axis='y', left=False, labelleft=False); ax.tick_params(axis='x', colors=INK2, labelsize=12)
cap = 'NASDAQ annual change · peak-to-trough -77.9% over 31 months' if EN else 'NASDAQ 年度跌幅 · 峰谷累计 -77.9%,历时 31 个月'
fig.text(.795, .20, cap, ha='center', fontsize=11.5, color=INK2, **({'family': 'DejaVu Sans'} if EN else {'fontproperties': CJK}))
out = ROOT / 'docs' / ('og-en.png' if EN else 'og.png'); out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=PAPER); print(out, out.stat().st_size, 'bytes')

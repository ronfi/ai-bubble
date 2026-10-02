#!/usr/bin/env python3
"""英文版同步检查:中文版由裁剪管线从源稿派生,英文版是人工翻译 —— 源稿一刷新,
英文版就会【静默过期】。本脚本按章比对哈希,指出哪几章需要重译。

  python3 tools/en_sync.py           # 检查,列出待重译的章;有漂移则非零退出
  python3 tools/en_sync.py --record  # 重译完成后记录当前中文各章哈希为"已同步"

哈希只对中文章节取,英文章按顺序一一对应(两版章数必须相等,不等即报错)。
"""
import sys, re, json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'data' / 'en_sync.json'

def chapters(md):
    """按 '## ' 切章;返回 [(标题, 正文哈希)]"""
    lines = md.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('## ')] + [len(lines)]
    return [(lines[idx[k]].lstrip('# ').strip(),
             hashlib.sha256('\n'.join(lines[idx[k]:idx[k + 1]]).encode()).hexdigest()[:16])
            for k in range(len(idx) - 1)]

zh = chapters((ROOT / 'REPORT.md').read_text(encoding='utf8'))
en_path = ROOT / 'REPORT.en.md'
if not en_path.exists():
    raise SystemExit('REPORT.en.md 不存在')
en = chapters(en_path.read_text(encoding='utf8'))
if len(zh) != len(en):
    raise SystemExit(f'🔴 章数不等:中文 {len(zh)} / 英文 {len(en)} —— 先对齐章结构再谈同步')

if '--record' in sys.argv:
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps({'synced': [h for _, h in zh], 'titles': [t for t, _ in zh]},
                                ensure_ascii=False, indent=1), encoding='utf8')
    print(f'✅ 已记录 {len(zh)} 章为"英文版已同步"')
    raise SystemExit(0)

if not STATE.exists():
    raise SystemExit('⚠ 无同步记录:重译完成后先跑一次 --record')
old = json.loads(STATE.read_text(encoding='utf8'))['synced']
stale = [zh[i][0] for i in range(len(zh)) if i >= len(old) or zh[i][1] != old[i]]
if stale:
    print(f'🔴 中文版有 {len(stale)} 章自上次同步后已改动,英文版对应章需重译:')
    for t in stale:
        print('   ·', t)
    print('\n(重译后跑 python3 tools/en_sync.py --record;在此之前英文页会自动挂"落后于中文版"提示)')
    sys.exit(1)
print(f'✅ 英文版与中文版同步({len(zh)} 章全部一致)')

import json
import os

p = 'lib.json'

def get_d():
    if os.path.exists(p) and os.path.getsize(p) > 0:
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
            for i, b in enumerate(d):
                if 'id' not in b: b['id'] = i + 1
                if 'rt' not in b: b['rt'] = 0
            return d
    return []

def sv_d(d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
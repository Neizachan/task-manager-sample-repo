"""Turn an axe JSON export into a triage table (rule, WCAG level, impact, nodes).  usage: python triage.py results/axe-none.json"""
import json, sys

ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}

def level(tags):
    if any(t.endswith("aa") and t.startswith("wcag") for t in tags): return "AA"
    if any(t.startswith("wcag") and t.endswith("a") for t in tags): return "A"
    return "best-practice"

rows = json.load(open(sys.argv[1], encoding="utf-8"))
rows.sort(key=lambda v: ORDER.get(v.get("impact"), 9))
print("| Rule | WCAG level | Impact | Elements | What it means |\n|---|---|---|---|---|")
for v in rows:
    print(f"| {v['id']} | {level(v['tags'])} | {v.get('impact')} | {len(v['nodes'])} | {v['help']} |")
print(f"\n{len(rows)} violated rules, {sum(len(v['nodes']) for v in rows)} elements")

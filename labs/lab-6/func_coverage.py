"""Per-function line coverage from a coverage.py JSON report. usage: python func_coverage.py cov.json"""
import ast, json, sys
TARGETS = {"app/storage.py": ["days_until_due", "build_query"], "app/cli.py": ["main"]}
cov = json.load(open(sys.argv[1]))
tot_s = tot_c = 0
for path, funcs in TARGETS.items():
    tree = ast.parse(open(path).read())
    executed = set(cov["files"][path]["executed_lines"]) if path in cov["files"] else set()
    missing = set(cov["files"][path]["missing_lines"]) if path in cov["files"] else set()
    stmts = executed | missing
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in funcs:
            lines = {l for l in stmts if node.lineno < l <= node.end_lineno}  # body only (excl. def line)
            c = len(lines & executed); tot_s += len(lines); tot_c += c
            print(f"{path}:{node.name:16s} {c}/{len(lines)} = {100*c/len(lines):.0f}%")
print(f"TARGET TOTAL {tot_c}/{tot_s} = {100*tot_c/tot_s:.0f}%")

"""Summarise cosmic-ray sessions, restricted to the three Lab 6 target functions. usage: python cr_summary.py <sqlite>..."""
import ast, sys
from cosmic_ray.work_db import use_db, WorkDB
TARGETS = {"app/storage.py": ["days_until_due", "build_query"], "app/cli.py": ["main"]}
def ranges(path):
    t = ast.parse(open(path).read()); return [(n.lineno, n.end_lineno) for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and n.name in TARGETS[path]]
tot = kill = 0; survivors = []
for db in sys.argv[1:]:
    with use_db(db, WorkDB.Mode.open) as w:
        for job, res in w.completed_work_items:
            for m in job.mutations:
                p = str(m.module_path).replace("\\", "/")
                if p in TARGETS and any(a <= m.start_pos[0] <= b for a, b in ranges(p)):
                    tot += 1
                    if res.test_outcome.name == "SURVIVED":
                        survivors.append(f"{p}:{m.start_pos[0]} {m.operator_name}#{m.occurrence}")
                    else: kill += 1
print(f"mutants={tot} killed={kill} survived={len(survivors)} score={100*kill/tot:.1f}%")
for s in survivors: print("  SURVIVED", s)

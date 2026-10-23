"""Export every logged decision (round, firm, price, message, reasoning) of each run to one CSV per run.
usage: python tools/export_decisions.py <out_dir> <run_dir> [<run_dir> ...]   (a run_dir holds <tag>/calls.jsonl, e.g. data/pilot/gemma4-12b_common_s1)"""
import csv, glob, json, os, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for run in sys.argv[2:]:
    for f in sorted(glob.glob(os.path.join(run, "*", "calls.jsonl"))):
        tag = os.path.basename(os.path.dirname(f))
        name = f"{os.path.basename(os.path.normpath(run))}__{tag}.csv"
        with open(os.path.join(out, name), "w", newline="", encoding="utf-8") as g:
            w = csv.writer(g)
            w.writerow(["round", "firm", "model", "price", "message", "reasoning", "flags"])
            for line in open(f, encoding="utf-8"):
                c = json.loads(line)
                w.writerow([c["round"], c["firm"], c["model"], c["price"], c["message"], c.get("reasoning") or "", ",".join(c["flags"])])

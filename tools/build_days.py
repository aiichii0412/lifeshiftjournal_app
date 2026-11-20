"""content/draft-*.md から app/data/days.js を作る(初回の変換用)。
以後は app/data/days.js を直接直してもよい。"""
import re, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
WEEKS = {1: "Let it Out", 2: "Notice Yourself", 3: "Be You Again", 4: "Step Forward"}
days = []
for f in ["content/draft-week1.md", "content/draft-week2-4.md"]:
    text = (root / f).read_text(encoding="utf-8")
    for sec in re.split(r"\n## ", "\n" + text)[1:]:
        lines = sec.split("\n")
        m = re.match(r"Day(\d+)\s+(.*)", lines[0])
        if not m:
            continue
        n, title = int(m.group(1)), m.group(2).strip()
        d = {"n": n, "week": (n - 1) // 7 + 1, "title": title, "guide": [], "work": "",
             "alt": [], "after": "", "pdf": None}
        mode, i = None, 1
        while i < len(lines):
            ln = lines[i].rstrip()
            if ln.startswith("**ひと言の案内**"): mode = "guide"
            elif ln.startswith("**本のワーク**"):
                d["work"] = ln.split(":", 1)[1].strip(); mode = None
            elif ln.startswith("**本がないときは**"): mode = "alt"
            elif ln.startswith("**📎"):
                mode = "pdf"
            elif ln.startswith("---") or ln.startswith("###"): break
            elif mode == "guide" and ln: d["guide"].append(ln)
            elif mode == "alt":
                if not ln: mode = "after"
                elif ln.startswith("　") and d["alt"]: d["alt"][-1] += "\n" + ln.strip("　")
                else: d["alt"].append(ln)
            elif mode == "after" and ln: d["after"] += (("\n" if d["after"] else "") + ln)
            elif mode == "pdf" and ln: d["pdf"] = {"title": ln, "url": ""}; mode = "after"
            i += 1
        days.append(d)
days.sort(key=lambda x: x["n"])
assert [d["n"] for d in days] == list(range(1, 29)), [d["n"] for d in days]
out = root / "app/data/days.js"
out.write_text("// 28日分の文章。ここを直すと、画面の文章が変わります。\nwindow.WEEKS = " +
               json.dumps(WEEKS, ensure_ascii=False) + ";\nwindow.DAYS = " +
               json.dumps(days, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print("ok", len(days), out.stat().st_size)

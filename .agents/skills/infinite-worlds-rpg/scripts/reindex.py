"""Build an offline line-addressable index from the packaged current pages."""
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def build():
    manifest=load("references/manifest.json"); keywords=load("references/keywords.json")
    rows=[]
    def add(kind,path,start,end,text,world=None,heading="",aliases=None):
        if not text.strip():return
        rows.append(dict(kind=kind,path=path,line_start=start,line_end=end,
            text=text,world_id=world,heading=heading,aliases=aliases or []))
    def index_file(path,mode,world=None):
        lines=(ROOT/path).read_text(encoding="utf-8").splitlines()
        heading="";para=[];first=0;last_header=""
        def flush():
            nonlocal para,first
            if para:
                add("evidence" if mode=="evidence" else ("rule" if mode=="rule" else "note"),
                    path,first,first+len(para)-1,"\n".join(para),world,heading)
                para=[]
        for i,line in enumerate(lines,1):
            if line.startswith("#"):
                flush(); heading=line.lstrip("# ");continue
            if not line.strip():flush();continue
            if line.startswith("|"):
                flush()
                if re.match(r"^\|[\s:|\-]+$",line):continue
                # A row directly preceding the separator is the table header.
                if i<len(lines) and re.match(r"^\|[\s:|\-]+$",lines[i]):last_header=line;continue
                kind="evidence" if mode=="evidence" else "entry"
                if mode=="rank" and re.match(r"^\| Rank\d+ \|",line):kind="rank"
                add(kind,path,i,i,line,world,heading)
                rows[-1]["table_header"]=last_header
                if kind=="rank":rows[-1]["rank"]=int(re.search(r"Rank(\d+)",line)[1])
                continue
            if not para:first=i
            para.append(line)
            if sum(map(len,para))>1200:flush()
        flush()
    for w in manifest["worlds"]:
        lines=(ROOT/w["path"]).read_text(encoding="utf-8").splitlines()
        add("world",w["path"],1,min(7,len(lines)),"\n".join(lines[:7]),w["id"],w["name"],w["aliases"])
        index_file(w["primary"],"primary",w["id"])
    for path in ["references/core-rules.md","references/prose-and-play.md","references/save-schema.md","references/retrieval.md"]:
        index_file(path,"rule")
    index_file("references/ranks.md","rank")
    for f in manifest["files"]:
        if f["role"]=="reference":index_file(f["path"],"evidence",f["world_id"])
    for t in keywords["topics"]:
        lines=(ROOT/t["path"]).read_text(encoding="utf-8").splitlines()
        start=next((i for i,l in enumerate(lines,1) if l.startswith("#") and t["section"] in l),1)
        end=min(len(lines),start+10)
        add("topic",t["path"],start,end,"\n".join(lines[start-1:end]),heading=t["section"],aliases=t["terms"])
    target=ROOT/"references/search-index.jsonl"
    target.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows),encoding="utf-8")
    return rows
if __name__=="__main__":
    from collections import Counter
    print(json.dumps(dict(records=len(r:=build()),by_kind=dict(Counter(x["kind"] for x in r))),ensure_ascii=True))


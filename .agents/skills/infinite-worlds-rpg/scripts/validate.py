"""Check portable references, packaged integrity and observable search behavior."""
from pathlib import Path
import hashlib,json,re,sys
from urllib.parse import unquote
from search import search,ROOT
def main():
    m=json.loads((ROOT/"references/manifest.json").read_text(encoding="utf-8"))
    assert len(m["worlds"])==24
    assert sum(w["declared_records"] for w in m["worlds"])==1619
    ranks=(ROOT/"references/ranks.md").read_text(encoding="utf-8")
    ids=[int(n) for n in re.findall(r"^\| Rank(\d+) \|",ranks,re.M)]
    assert ids==list(range(126))
    for f in m["files"]:
        assert hashlib.sha256((ROOT/f["path"]).read_bytes()).hexdigest()==f["packaged_sha256"],f["path"]
    links=0
    for f in ROOT.rglob("*.md"):
        for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^\n]+?)\)",f.read_text(encoding="utf-8")):
            if re.match(r"[a-zA-Z]+://",target) or target.startswith("#"):continue
            target=unquote(target.strip("<>").split("#")[0])
            dest=(f.parent/target).resolve()
            assert dest.is_relative_to(ROOT.resolve()),(f,target,"not portable")
            assert dest.exists(),(f,target,"missing")
            links+=1
    rows=[json.loads(l) for l in (ROOT/"references/search-index.jsonl").read_text(encoding="utf-8").splitlines()]
    cache={}
    for r in rows:
        p=r["path"]
        if p not in cache:cache[p]=(ROOT/p).read_text(encoding="utf-8").splitlines()
        assert "\n".join(cache[p][r["line_start"]-1:r["line_end"]])==r["text"],(p,r["line_start"])
    for n in [0,4,44,76,93,125]:
        got=search("Rank"+str(n),kind="rank")["hits"]
        assert len(got)==1 and got[0]["rank"]==n,(n,got)
    got=search("凝气1层",world="仙逆")["hits"]
    assert got and "XN001" in got[0]["text"],got
    got=search("仙帝",world="完美世界")["hits"]
    assert got and "| emperor |" in got[0]["text"],got
    got=search("前传 Therion",world="Demonbane",kind="entry")["hits"]
    assert got and any("DBC-26" in x["text"] and "Rank76+" in x["text"] for x in got)
    got=search("Z2",world="龙珠")["hits"]
    assert got and all(x["world_id"]==9 for x in got)
    got=search("阿撒托斯",world="克苏鲁")["hits"]
    assert got and all(x["world_id"]==15 for x in got)
    got=search("阿撒托斯",world="斩魔大圣")["hits"]
    assert got and all(x["world_id"]==24 for x in got)
    got=search("学员",limit=50)["hits"]
    assert len({x["world_id"] for x in got if x["world_id"]})>=3
    got=search("跨主世界 权限")["hits"]
    assert got and any("core-rules.md" in x["path"] for x in got)
    assert all(x["kind"]!="evidence" for x in search("Rank44",limit=50)["hits"])
    assert "error" in search("test",world="不存在的世界")
    print(json.dumps(dict(status="pass",worlds=24,declared_records=1619,ranks=126,
        indexed_segments=len(rows),verified_links=links,integrity_files=len(m["files"]),search_checks="passed"),ensure_ascii=True))
if __name__=="__main__":main()

"""Search this skill offline. Results are pointers, never automatic adjudications."""
from pathlib import Path
import argparse, json, re, unicodedata, sys
ROOT=Path(__file__).resolve().parents[1]
def norm(s):
    s=unicodedata.normalize("NFKC",s).casefold()
    digits={c:i for i,c in enumerate("零一二三四五六七八九")}
    def stage_number(match):
        value=match[1]
        if value.isdigit():return value
        if "十" in value:
            left,right=value.split("十",1)
            return str((digits.get(left,1) if left else 1)*10+(digits.get(right,0) if right else 0))
        return str(digits[value]) if value in digits else value
    s=re.sub(r"第?([零一二三四五六七八九十\d]+)(?=层|阶|段|重|口)",stage_number,s)
    return re.sub(r"[\s·・_\-—：:，,。！!（）()]+","",s)
def resources():
    kw=json.loads((ROOT/"references/keywords.json").read_text(encoding="utf-8"))
    rows=[json.loads(l) for l in (ROOT/"references/search-index.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return kw,rows
def search(query="",world=None,kind=None,evidence=False,limit=8):
    kw,rows=resources(); world_ids=None
    if world:
        world_ids={w["id"] for w in kw["worlds"] if norm(world) in {norm(str(w["id"])),norm(w["name"]),*(norm(a) for a in w["aliases"])}}
        if not world_ids:
            return dict(query=query,world=world,error="世界未匹配；请查世界索引或使用完整作品名。",hits=[])
        if len(world_ids)>1:
            return dict(query=query,world=world,error="该别名对应多个世界；请指定作品。",candidates=[w["name"] for w in kw["worlds"] if w["id"] in world_ids],hits=[])
    if world and not query and not kind:kind="world"
    raw=norm(query); variants={raw} if raw else set()
    for group in kw["synonyms"]:
        for term in group:
            n=norm(term)
            if n and n in raw:
                variants.update(raw.replace(n,norm(other)) for other in group)
    tokens=[norm(t) for t in re.split(r"\s+",query.strip()) if norm(t)]
    rank_request=re.search(r"(?i)\b(?:rank|r)\s*(\d{1,3})(?!\d)",query)
    explicit_rank=int(rank_request[1]) if rank_request else None
    results=[]
    for row in rows:
        if world_ids is not None and row["world_id"] not in world_ids:continue
        if kind and row["kind"]!=kind:continue
        if row["kind"]=="evidence" and not evidence and kind!="evidence":continue
        if explicit_rank is not None:
            if row["kind"]=="rank" and row["rank"]!=explicit_rank:continue
            mentioned={int(n) for n in re.findall(r"(?i)rank\s*(\d{1,3})(?!\d)",row["text"]+" "+" ".join(row.get("aliases",[])))}
            if explicit_rank not in mentioned:continue
        hay=norm(row["text"]+" "+row.get("heading",""))
        alias=[norm(x) for x in row.get("aliases",[])]
        score=0
        if not raw:
            if row["kind"]=="world" or kind:score=1
            else:continue
        else:
            if any(q and q in hay for q in variants):score+=100
            if raw in alias:score+=130
            elif any(a and a in raw for a in alias):score+=25
            matched=sum(t in hay for t in tokens)
            if tokens and matched==len(tokens):score+=40
            elif matched:score+=8*matched
            # CJK character pairs provide fallback for natural-language questions.
            if score==0 and len(raw)>=3:
                pairs={raw[i:i+2] for i in range(len(raw)-1) if all("\u4e00"<=c<="\u9fff" for c in raw[i:i+2])}
                overlap=sum(t in hay for t in pairs)
                if pairs and overlap>=2 and overlap/len(pairs)>=0.4:score+=overlap
            if score==0:continue
        if row["kind"] in {"entry","rank"}:score+=5
        if row["kind"]=="entry" and raw:
            cells=[x.strip() for x in row["text"].strip("|").split("|")]
            header=[x.strip().casefold() for x in row.get("table_header","").strip("|").split("|")]
            pos=1 if header and header[0] in {"id","编号","记录id"} else 0
            label=cells[pos] if len(cells)>pos else ""
            base=re.split(r"[·（(／/]",label,1)[0]
            if norm(label) in variants or norm(cells[0]) in variants:score+=200
            elif norm(base) in variants:score+=100
            if norm(base) in variants and "原锚：" in row["text"]:score+=20
        if row["kind"]=="evidence":score-=5
        if world and raw and row["kind"]=="world":score*=0.1
        copy=dict(row);copy["score"]=score;results.append(copy)
    results.sort(key=lambda x:(-x["score"],x["path"],x["line_start"]))
    return dict(query=query,world=world,matched=len(results),hits=results[:max(1,min(limit,50))])
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query",nargs="?",default="")
    parser.add_argument("--world")
    parser.add_argument("--kind",choices=["world","rank","entry","rule","note","topic","evidence"])
    parser.add_argument("--evidence",action="store_true")
    parser.add_argument("--limit",type=int,default=8)
    args=parser.parse_args()
    if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(search(**vars(args)),ensure_ascii=False,indent=2))
if __name__=="__main__":main()

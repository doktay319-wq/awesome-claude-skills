import json
R="/home/user/awesome-claude-skills/zouff-mission3"
d=json.load(open(f"{R}/mission3.json",encoding="utf-8"))
seen=set(); cards=[]
def add(kind,x):
    fr,nl,tr=x["fr"].strip(),x["nl"].strip().replace(" (FR)",""),x["tr"].strip()
    if not fr or not nl or not tr: return
    k=(fr.lower(),nl.lower())
    if k in seen: return
    seen.add(k)
    cards.append(dict(id=f"{kind[0]}{len(cards)+1:03d}",page=x["page"],kind=kind,fr=fr,nl=nl,tr=tr))
for x in d["vocab"]: add("word",x)
for x in d["phrases"]:
    if x["src"].startswith(("Dit heb ik","Ex 18a","Ex 18c","Ex 18d","Ex 19a")): continue
    add("phrase",x)
cards.sort(key=lambda c:(c["page"] if c["page"] else 99, c["id"]))
# stable ids already assigned; sort changes order only
data=json.dumps(cards,ensure_ascii=False,separators=(",",":"))
head=open(R+"/app/src/head.html",encoding="utf-8").read()
body=open(R+"/app/src/body.html",encoding="utf-8").read().replace("/*__DATA__*/[]",data)
open(R+"/app/zouff-artifact.html","w",encoding="utf-8").write(head+body)
full=('<!doctype html>\n<html lang="tr"><head><meta charset="utf-8">'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Zouff">'
 '<meta name="theme-color" content="#0E8A8C">\n'+head+'<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>\n</head><body>\n'+body+'</body></html>\n')
import os; os.makedirs(f"{R}/app",exist_ok=True)
open(f"{R}/app/index.html","w",encoding="utf-8").write(full)
print(len(cards),"cards",len(full)//1024,"KB")

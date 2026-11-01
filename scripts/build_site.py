from pathlib import Path
import html,csv,re,json
R=Path(__file__).resolve().parents[1];S=R/'site';S.mkdir(exist_ok=True)
css='body{font-family:system-ui,-apple-system,"Noto Sans JP",sans-serif;background:#f7f9fc;color:#1a2a3b;line-height:1.75;margin:auto;max-width:1000px;padding:26px}a{color:#135c94}header{border-bottom:2px solid #27678e;padding-bottom:12px;margin-bottom:20px}article{background:white;border-radius:12px;padding:20px;margin:16px 0;border:1px solid #dce5ec}small{color:#5a6672}.warning{background:#fff2d9;border-left:4px solid #cf9631;padding:12px}input{width:100%;padding:12px;border:1px solid #abbcc8;border-radius:8px}li{margin-bottom:7px}pre{white-space:pre-wrap}'
(S/'style.css').write_text(css)
files=sorted((R/'textbook').glob('*.md'))
nav=''.join(f'<li><a href="{f.stem}.html">{html.escape(f.read_text().splitlines()[0].lstrip("# "))}</a></li>' for f in files)
def shell(title,body):return f'<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="stylesheet" href="style.css"><header><a href="index.html">乳児頭蓋変形 Evidence Hub</a></header>{body}</html>'
for file in files:
 lines=file.read_text(encoding='utf-8').splitlines()
 out=[]
 for line in lines:
  if not line.strip():continue
  if line.startswith('# '):out.append('<h1>'+html.escape(line[2:])+'</h1>')
  elif line.startswith('## '):out.append('<h2>'+html.escape(line[3:])+'</h2>')
  else:out.append('<p>'+html.escape(line)+'</p>')
 (S/(file.stem+'.html')).write_text(shell(file.stem,'<article>'+''.join(out)+'</article>'),encoding='utf-8')
with (R/'literature'/'papers.csv').open(encoding='utf-8-sig') as f: papers=list(csv.DictReader(f))
# Only include trusted http(s) href targets from original fields.
def safe_url(u):return u if u.startswith('https://') or u.startswith('http://') else ''
entries=[]
for r in papers:
 link=safe_url(r.get('記事URL',''))
 entries.append({'title':r['タイトル'],'year':r.get('年',''),'category':r.get('テーマ',''),'oa':r.get('Open Access',''),'url':link})
json_data=json.dumps(entries,ensure_ascii=False).replace('<','\u003c')
js='const entries='+json_data+';const list=document.getElementById("results"),input=document.getElementById("filter");function draw(){let q=input.value.toLowerCase();let v=entries.filter(x=>(x.title+" "+x.year+" "+x.category).toLowerCase().includes(q));list.replaceChildren(...v.slice(0,300).map(x=>{let li=document.createElement("li"),a=document.createElement("a");a.textContent=x.title+" ("+x.year+") "+x.category;if(x.url){a.href=x.url;a.target="_blank";a.rel="noopener noreferrer";}li.appendChild(a);return li}));document.getElementById("count").textContent=v.length+"件（先頭300件まで表示）"}input.addEventListener("input",draw);draw();'
(S/'papers.html').write_text(shell('文献リスト',f'<h1>文献検索</h1><p>Google SheetsのPapersタブから公開用列のみを抽出。計{len(entries)}件。</p><input id="filter" placeholder="タイトル・年・テーマで検索"><p id="count"></p><ol id="results"></ol><script>{js}</script>'),encoding='utf-8')
(S/'index.html').write_text(shell('乳児頭蓋変形 Evidence Hub','<h1>乳児頭蓋変形 Evidence Hub</h1><p>AIエージェントによる文献統合型テキストブック。継続更新予定。</p><div class="warning">本内容はAI生成の研究用改訂作業版です。専門家の独立査読は未実施です。医学的判断の代替にはなりません。出典と原著を確認してください。</div><article><h2>テキストブック</h2><ol>'+nav+'</ol></article><article><h2><a href="papers.html">文献リストを検索</a></h2><p>原著へのリンク、OA確認状況を公開しています。</p></article><small>初期資料: 2026-10-31 / 更新はGitHubの履歴を参照</small>'),encoding='utf-8')
print('site generated',len(files),'chapters',len(entries),'papers')

#!/usr/bin/env python3
"""Sync Google Doc and Sheets Papers tab into chapter Markdown/CSV files."""
import os,io,csv,re,pathlib
import google.auth
from googleapiclient.discovery import build

ROOT=pathlib.Path(__file__).resolve().parents[1]
DOC=os.getenv('GOOGLE_DOC_ID','10urKQXlpjne33hfY7R_MbwpwKkeesQXQsIpwDn-e_c0')
SHEET=os.getenv('GOOGLE_SHEET_ID','1cfTCAXQ2Bu_j1yn_7BkroMqfxlCzwGO2Rn_wvp6uWrQ')
cred,_=google.auth.default(scopes=['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/spreadsheets.readonly'])
drive=build('drive','v3',credentials=cred,cache_discovery=False)
sheets=build('sheets','v4',credentials=cred,cache_discovery=False)
raw=drive.files().export(fileId=DOC,mimeType='text/plain').execute()
text=raw.decode('utf-8-sig') if isinstance(raw,bytes) else str(raw)
sections={0:[]};section=0
for line in text.splitlines():
 t=line.strip()
 if not t:continue
 m=re.match(r'^第\s*([0-9０-９]+)\s*章',t)
 if m:
  section=int(m.group(1).translate(str.maketrans('０１２３４５６７８９','0123456789')))
  sections.setdefault(section,[])
 sections[section].append(t)
if len([x for x in sections if x>0])<12:raise ValueError('Expected 12 textbook chapters; aborting without altering site')
for idx,lines in sections.items():
 out=ROOT/'textbook'/(f'{idx:02d}.md' if idx else '00-introduction.md')
 out.write_text('\n\n'.join(('# '+lines[0] if j==0 or (idx==0 and j==0) else '## '+line if line in ('参考文献','本章の要点') else line) for j,line in enumerate(lines))+'\n',encoding='utf-8')
values=sheets.spreadsheets().values().get(spreadsheetId=SHEET,range='Papers!A:Q').execute().get('values',[])
header=values[0]
fields=['優先','テーマ','タイトル','著者','年','Journal','種別','主題','Open Access','記事URL','PDF URL','Summary Status']
indexes=[header.index(x) for x in fields]
records=[[row[i] if i<len(row) else '' for i in indexes] for row in values[1:] if len(row)>2 and row[2].strip()]
if len(records)<100:raise ValueError('Suspiciously small Papers sheet, refusing update')
with (ROOT/'literature'/'papers.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(fields);writer.writerows(records)
print(f'Synced {len(sections)-1} chapters and {len(records)} literature entries')

#!/usr/bin/env python3
"""Write a concise PR summary from git changes; risk keywords are triage hints, not clinical validation."""
import subprocess
from pathlib import Path

def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout

changes = git("diff", "--name-only", "HEAD", "--", "textbook", "literature").splitlines()
chapters = [f for f in changes if f.startswith("textbook/")]
papers = "literature/papers.csv" in changes
patch = git("diff", "--unified=0", "HEAD", "--", "textbook")
added = [x[1:] for x in patch.splitlines() if x.startswith("+") and not x.startswith("+++")]
removed = [x[1:] for x in patch.splitlines() if x.startswith("-") and not x.startswith("---")]
terms = ["推奨", "禁忌", "安全", "有害", "リスク", "適応", "死亡", "窒息", "効果", "合併症", "副作用", "重症", "治療開始", "治療終了"]
signals = sorted({term for term in terms if any(term in row for row in added + removed)})
lines = [
    "# Google Drive同期：変更概要",
    "",
    "この概要は機械的な差分抽出です。医学的妥当性や引用の正しさは検証していません。",
    "",
    f"- 変更ファイル: {len(changes)}件（本文 {len(chapters)}件、文献CSV {'更新あり' if papers else '変更なし'}）",
    f"- 本文の追加行: {len(added)}、削除行: {len(removed)}（Markdownの行単位）",
    "- 変更章: " + (", ".join(chapters) if chapters else "なし"),
    "- 要注意語の出現: " + (", ".join(signals) if signals else "検出なし（安全を保証しません）"),
    "",
    "## 公開前の確認",
    "- [ ] 医学的推奨、治療適応、安全性、数値の重要変更がないか確認",
    "- [ ] 出典と本文の対応、文献の重複や削除を確認",
    "- [ ] テキストブックの章数・表・末尾の欠落がないことを確認",
    "",
    "HTMLはPRに含めません。サイトはmainへのマージ後、Pagesのワークフロー内で生成します。",
    "",
]
Path("REVIEW_SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))

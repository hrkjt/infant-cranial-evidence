# 乳児頭蓋変形 Evidence Hub

AIエージェントが生成する乳児頭蓋変形の文献統合テキストブックの公開用リポジトリです。

- `textbook/`：章別の本文。2026-10-31版を初期資料として収録
- `literature/papers.csv`：Papersシートから公開向けの項目のみ抽出
- `scripts/sync_drive.py`：Google Driveの最新版を取得して更新
- `.github/workflows/sync.yml`：毎日同期して差分があればPull Requestを作成
- `.github/workflows/pages.yml`：mainに反映した内容をGitHub Pagesへ公開

**注意**：AI生成の改訂作業版であり、専門家レビュー済み・診療ガイドラインではありません。文献情報、引用、医学的表現は原著で確認してください。非OA文献の本文を確認したとは限りません。

## 初期設定

1. 新しい**公開リポジトリ**を作成し、このフォルダの内容をコミットする（既存の医療データ用リポジトリに混ぜない）。
2. Google CloudでDrive APIを有効化しサービスアカウントを作成。対象のGoogle Doc/Sheetをサービスアカウントのメールへ閲覧共有する。
3. GitHub Actions secret `GOOGLE_SERVICE_ACCOUNT_JSON` にサービスアカウント鍵JSONを登録（鍵はリポジトリへ保存しない）。
4. Repository Settings → Actions → General → Workflow permissions でPR作成に必要な権限を設定する。組織のポリシーが許す場合に限る。
5. Settings → Pages → Build and deployment → Source を `GitHub Actions` にする。
6. Actionsの `Sync from Google Drive` を手動実行し、作成されたPRを確認・マージする。
7. 定期実行は毎日 01:00 UTC（10:00 JST）。GitHub Actionsのscheduleは遅延・スキップする場合がある。

初期資料は2026-10-31時点のスナップショットから作成。以後の同期先は既定のGoogle Docs/Sheetsであり、ファイルIDを変更する場合はworkflowの環境変数を変更する。

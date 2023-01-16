# slack-export-spreadsheet
## 使い方
- このリポジトリをクローン
```bash
git clone https://github.com/seiya8/slack-export-spreadsheet.git
cd slack-export-spreadsheet
```
- 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```
- [Slack API tokenの取得方法](./docs/slack_api.md)に従って、tokenを取得
- [Google サービスアカウントキーの取得方法](./docs/google_drive_api.md)に従ってJSONファイルをダウンロード。
- [Google Driveフォルダの設定](./docs/drive_folder.md)に従ってフォルダを共有し、フォルダのIDを取得。
- スクリプトを実行
```bash
bash run.sh
```
順番にtokenとJSONファイルとDriveフォルダIDを聞かれるので、答えるとエクスポートが始まる。
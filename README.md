# slack-export-spreadsheet
SlackからSlack APIを使ってチャンネル履歴を取得し、スプシを作るコードです。スレッドの返信も取得します。添付ファイルはドライブにアップされ、スプシにはそのリンクが貼られます。
スプシの各シートが各チャンネルの履歴に対応しています。

## 使い方
- このリポジトリをクローンする。 Clone this repository.
```bash
git clone https://github.com/seiya8/slack-export-spreadsheet.git
cd slack-export-spreadsheet
```
- 必要なパッケージをインストール。 Install the required packages via pip.
```bash
pip install -r requirements.txt
```
- [Slack API tokenの取得方法](./docs/slack_api.md)に従って、tokenを取得。
- [Google サービスアカウントキーの取得方法](./docs/google_drive_api.md)に従ってJSONファイルをダウンロード。
- [Google Driveフォルダの設定](./docs/drive_folder.md)に従ってフォルダを共有し、フォルダのIDを取得。
- スクリプトを実行。 Execute the shell script.
```bash
bash run.sh
```
順番にtokenとJSONファイルとDriveフォルダIDを聞かれるので、答えるとエクスポートが始まる。

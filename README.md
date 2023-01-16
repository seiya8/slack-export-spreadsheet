# slack-export-spreadsheet
SlackからSlack APIを使ってパブリックチャンネルの履歴を取得し、スプシを作るコードです。スレッドの返信も取得します。添付ファイルはドライブにアップされ、スプシにはそのリンクが貼られます。
スプシの各シートが各チャンネルの履歴に対応しています。

This code downloads the public-channel histories of Slack via Slack API and creates a spreadsheet. Thread replies are also included. Attached files are uploaded to the Google Drive and links to them are put in the spreeadsheet. Each sheet of the spreeadsheet corresponds to the history of each channel.

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
- [Slack API tokenの取得方法](./docs/slack_api.md)に従って、tokenを取得。Get a slack api token.
- [Google サービスアカウントキーの取得方法](./docs/google_drive_api.md)に従ってJSONファイルをダウンロード。 Create a Google service account and download a JSON file containing a secret key.
- [Google Driveフォルダの設定](./docs/drive_folder.md)に従ってフォルダを共有し、フォルダのIDを取得。 Create a folder in Google Drive, share it with the service acount, and get the folder ID from URL.
- スクリプトを実行。 Execute the shell script.
```bash
bash run.sh
```
順番にtokenとJSONファイルとDriveフォルダIDを聞かれるので、答えるとエクスポートが始まる。

# Google サービスアカウントキーの取得方法
- https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts を開き、`プロジェクトを作成`。
![image](./figures/google_api00.png)
- プロジェクト名を入力し、作成。
![image](./figures/google_api01.png)
上の検索窓でsheetsと入力し、Google Sheets APIを選択。
![image](./figures/google_api02.png)
Google Sheets APIを有効にする。
![image](./figures/google_api03.png)
同様に、Google Drive APIを有効にする。
![image](./figures/google_api04.png)
![image](./figures/google_api05.png)
`認証情報を作成` をクリック。
![image](./figures/google_api06.png)
`サービスアカウント` を選択。
![image](./figures/google_api07.png)
サービスアカウント名を入力し、`完了` を押す。
![image](./figures/google_api08.png)
作成したサービスアカウントのメールアドレスを選択。
![image](./figures/google_api09.png)
`鍵を追加`
![image](./figures/google_api10.png)
`作成`
![image](./figures/google_api11.png)
JSONファイルがダウンロードされる。ダウンロードしたJSONファイルを適当なディレクトリに移動しておく。

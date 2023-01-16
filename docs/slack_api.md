# Slack API tokenの取得方法
- https://api.slack.com/apps から `Create New App`をクリック。
![image](./figures/slack_api0.png)
<br>
- `From scratch` をクリック。
![image](./figures/slack_api1.png)
<br>
- `App Name` を入力。インストールするワークスペースを選択し、`Create App` をクリック。
- `Add features and functionality` の `Permissions` をクリック。
![image](./figures/slack_api2.png)
<br>
- `Scopes` の `User Token Scopes` に以下を追加。
  - `channels:history`
  - `channels:read`
  - `files:read`
  - `users:read`
![image](./figures/slack_api3.png)
<br>
- 下の画像のようになっていればOK
![image](./figures/slack_api4.png)
<br>
- `Install to Workspace` をクリック。
![image](./figures/slack_api5.png)
<br>
- tokenが生成されるのでそれをクリップボードにコピー。
![image](./figures/slack_api6.png)

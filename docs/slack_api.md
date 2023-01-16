# Slack API tokenの取得方法
- https://api.slack.com/apps から `Create New App`
![image](./figures/slack_api0.png)

- `From scratch` でアプリを作る。
![image](./figures/slack_api1.png)

- `App Name` を入力。インストールするワークスペースを選択し、`Create App`
- `Add features and functionality` の `Permissions` をクリック。
![image](./figures/slack_api2.png)

- `Scopes` の `User Token Scopes` に以下を追加。
  - `channels:history`
  - `channels:read`
  - `files:read`
  - `users:read`
![image](./figures/slack_api3.png)

- 下の画像のようになっていればOK
![image](./figures/slack_api4.png)

- `Install to Workspace`
![image](./figures/slack_api5.png)

- tokenが生成されるのでそれをクリップボードにコピー。
![image](./figures/slack_api6.png)

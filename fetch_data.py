import codecs
import json
import os
import requests
import time

token = ""
headers = {"Authorization": f"Bearer {token}"}

# チャンネルリスト取得し、ディレクトリ作成
response_json = requests.get("https://slack.com/api/conversations.list", headers=headers).json()

ch_id_dict = {}
for ch_dict in response_json["channels"]:
    ch_name = ch_dict["name"]
    ch_id_dict[ch_dict["id"]] = ch_name
    os.makedirs(ch_name, exist_ok=True)

with open("channels.json", "w") as f:
    json.dump(ch_id_dict, f, indent=2)

# メッセージ取得
for ch_id, ch_name in ch_id_dict.items():
    print(ch_name)
    # 最大1000件, 履歴の開始日時は指定しない
    params = {"channel": ch_id, "limit": "1000", "oldest": "0"}

    # チャンネルの履歴を取得
    message_list = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params).json()["messages"]

    message_save_list = []
    for message in message_list:
        ts = message["ts"]
        reply_params = {"channel": ch_id, "ts": ts}
        
        time.sleep(1)
        reply_list = requests.get("https://slack.com/api/conversations.replies", headers=headers, params=reply_params).json()["messages"]

        for reply_dict in reply_list:
            if 'files' in reply_dict:
                for file_dict in reply_dict["files"]:
                    dl_url = file_dict["url_private_download"]

                    time.sleep(1)
                    content = requests.get(dl_url, allow_redirects=True, headers=headers, stream=True).content

                    filename = file_dict["name"]
                    save_dirname = os.path.join(ch_name, reply_dict["ts"])
                    os.makedirs(save_dirname, exist_ok=True)
                    with codecs.open(os.path.join(save_dirname, filename), "wb") as f:
                        f.write(content)


        with open('a.json', 'w') as f:
            json.dump(reply_list, f, ensure_ascii=False, indent=2)

        message_save_list.append(reply_list)

    path = os.path.join(ch_name, f"{ch_name}_channel_hist.json")

    with open(path, "w") as f:
        json.dump(message_save_list, f, sort_keys=True, ensure_ascii=False, indent=2)

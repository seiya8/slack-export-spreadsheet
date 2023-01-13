import requests
import json
import time

token = ""
headers = {"Authorization": f"Bearer {token}"}

# チャンネルリスト取得し、ディレクトリ作成
time.sleep(1)
members_list = requests.get("https://slack.com/api/users.list", headers=headers).json()["members"]

member_save_dict = {}
for member_dict in members_list:
    if not member_dict['deleted'] and member_dict['is_email_confirmed']:
        member_save_dict[member_dict['id']] = member_dict['real_name']

with open('users.json', 'w') as f:
    json.dump(member_save_dict, f, ensure_ascii=False, indent=2)

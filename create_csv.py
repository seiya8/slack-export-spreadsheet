import os
import json
import csv
from datetime import datetime

with open('channels.json', 'r') as f:
    ch_dict = json.load(f)

with open('users.json', 'r') as f:
    usr_id2name = json.load(f)

for ch_name in ch_dict.values():
    with open(os.path.join(ch_name, f"{ch_name}_channel_hist.json"), 'r') as f:
        msg_list = json.load(f)
        
    with open(f'{ch_name}.csv', 'w') as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', lineterminator='\n')
        # writer.writerow(["time", "name", "post", "files", "reply"])

        for thread in msg_list:
            for i, msg in enumerate(thread):
                post_time = datetime.fromtimestamp(int(float(msg['ts']))).strftime('%Y-%m-%d %H:%M')
                name = usr_id2name[msg['user']]
                if i:
                    post = ''
                    reply = msg['text']
                else:
                    post = msg['text']
                    reply = ''

                for k, v in usr_id2name.items():
                    post = post.replace(k, v)
                    reply = reply.replace(k, v)

                files_name = '\n'.join(map(lambda x: x['url_private_download'], msg['files'])) if 'files' in msg.keys() else ''

                writer.writerow([post_time, name, post, files_name, reply])

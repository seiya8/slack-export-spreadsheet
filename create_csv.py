import os
import json
import csv
from datetime import datetime

with open('channels.json', 'r') as f:
    channel_dict = json.load(f)

with open('users.json', 'r') as f:
    user_dict = json.load(f)

os.makedirs('output/csv_files', exist_ok=True)
for channel_name in channel_dict.values():
    with open(os.path.join('output', 'json_files', f'{channel_name}_message.json'), 'r') as f:
        message_list = json.load(f)
        
    with open(os.path.join('output', 'csv_files', f'{channel_name}.csv'), 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')

        for thread in message_list:
            for i, message in enumerate(thread):
                post_time = datetime.fromtimestamp(int(float(message['ts']))).strftime('%Y-%m-%d %H:%M')
                name = user_dict[message['user']]
                post = '' if i else message['text']
                reply = message['text'] if i else ''

                for user_id, user_name in user_dict.items():
                    post = post.replace(user_id, user_name)
                    reply = reply.replace(user_id, user_name)

                files_name = '\n'.join(map(lambda x: x['url_private_download'], message['files'])) if 'files' in message.keys() else ''
                writer.writerow([post_time, name, post, files_name, reply])

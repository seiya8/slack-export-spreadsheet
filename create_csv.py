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

                if 'files' in message:
                    dirname = os.path.join('output', 'attached_files', channel_name, message['ts'])
                    for i, file in enumerate(message['files']):
                        file_name = os.path.join(dirname, file['name'])
                        if not i:
                            writer.writerow([post_time, name, post, file_name, reply])
                        else:
                            writer.writerow([post_time, name, '', file_name, ''])

                else:
                    writer.writerow([post_time, name, post, '', reply])

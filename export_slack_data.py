import codecs
import csv
from datetime import datetime
import json
import os
import requests
import sys
import time

def dump_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_user(headers):
    time.sleep(1)
    response_json = requests.get('https://slack.com/api/users.list', headers=headers).json()
    return response_json['members']

def parse_user_json(headers):
    user_list = fetch_user(headers)

    user_id_name_dict = {}
    for user_dict in user_list:
        user_id_name_dict[user_dict['id']] = user_dict['profile']['real_name']
    return user_id_name_dict

def fetch_channel(headers):
    time.sleep(1)
    response_json = requests.get('https://slack.com/api/conversations.list', headers=headers).json()
    return response_json['channels']

def parse_channel_json(headers):
    channel_list = fetch_channel(headers)

    ch_id_name_dict = {}
    for channel_dict in channel_list:
        channel_name = channel_dict['name']
        ch_id_name_dict[channel_dict['id']] = channel_name
    return ch_id_name_dict

def fetch_message(headers, params):
    time.sleep(1)
    response_json = requests.get('https://slack.com/api/conversations.history', headers=headers, params=params).json()
    return response_json['messages']

def fetch_reply(headers, params):
    time.sleep(1)
    response_json = requests.get('https://slack.com/api/conversations.replies', headers=headers, params=params).json()
    return response_json['messages']

def fetch_file(url, headers):
    time.sleep(1)
    return requests.get(url, allow_redirects=True, headers=headers, stream=True).content

def save_file(data, file_path):
    with codecs.open(file_path, 'wb') as f:
        f.write(data)

def get_thread_list(headers, params):
    message_list = fetch_message(headers, params)
    all_thread_list = []
    for message_dict in message_list:
        ts = message_dict['ts']
        reply_params = {'channel': params['channel'], 'ts': ts}
        reply_list = fetch_reply(headers, reply_params)
        all_thread_list.append(reply_list)
    return all_thread_list

def download_files(channel_name, thread_list):
    for thread in thread_list:
        for message_dict in thread:
            if 'files' not in message_dict: continue
            for file_dict in message_dict['files']:
                dl_url = file_dict['url_private_download']
                content = fetch_file(dl_url, headers)

                save_dirname = os.path.join('output', 'attached_files', channel_name, message_dict['ts'])
                os.makedirs(save_dirname, exist_ok=True)
                save_file(content, os.path.join(save_dirname, file_dict['name']))

def create_csv(channel_name, user_dict, thread_list):
    with open(os.path.join('output', 'csv_files', f'{channel_name}.csv'), 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for thread in thread_list:
                for i, message in enumerate(thread):
                    post_time = datetime.fromtimestamp(int(float(message['ts']))).strftime('%Y-%m-%d %H:%M')
                    name = user_dict[message['user']]
                    post = '' if i else message['text']
                    reply = message['text'] if i else ''

                    for user_id, user_name in user_dict.items():
                        post = post.replace(user_id, user_name)
                        reply = reply.replace(user_id, user_name)

                    file_name = ''
                    if 'files' in message:
                        dirname = os.path.join('output', 'attached_files', channel_name, message['ts'])
                        for i, file in enumerate(message['files']):
                            file_name = os.path.join(dirname, file['name'])
                            if i: post, reply = '', ''
                            writer.writerow([post_time, name, post, file_name, reply])
                    else:
                        writer.writerow([post_time, name, post, file_name, reply])

if __name__ == '__main__':
    os.makedirs('output/json_files', exist_ok=True)
    os.makedirs('output/csv_files', exist_ok=True)

    headers = {'Authorization': f'Bearer {sys.argv[1]}'}

    user_dict = parse_user_json(headers)
    dump_json(user_dict, 'users.json')
    channel_dict = parse_channel_json(headers)
    dump_json(channel_dict, 'channels.json')
    
    for channel_id, channel_name in channel_dict.items():
        print(f'channel: {channel_name}')

        params = {'channel': channel_id, 'limit': '1000', 'oldest': '0'}
        thread_list = get_thread_list(headers, params)

        os.makedirs(f'output/attached_files/{channel_name}', exist_ok=True)
        save_message_path = os.path.join('output/json_files', f'{channel_name}.json')
        dump_json(thread_list, save_message_path)
        create_csv(channel_name, user_dict, thread_list)
        download_files(channel_name, thread_list)

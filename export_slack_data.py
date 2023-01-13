import codecs
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
            if 'files' in message_dict:
                for file_dict in message_dict['files']:
                    dl_url = file_dict['url_private_download']
                    content = fetch_file(dl_url, headers)

                    save_dirname = os.path.join(channel_name, message_dict['ts'])
                    os.makedirs(save_dirname, exist_ok=True)
                    save_file(content, os.path.join(save_dirname, file_dict['name']))

if __name__ == '__main__':
    token = sys.argv[1]
    headers = {'Authorization': f'Bearer {token}'}
    print(token)
    user_dict = parse_user_json(headers)
    dump_json(user_dict, 'users.json')
    channel_dict = parse_channel_json(headers)
    dump_json(channel_dict, 'channels.json')
    
    for channel_id, channel_name in channel_dict.items():
        print(channel_name)
        os.makedirs(channel_name, exist_ok=True)

        params = {'channel': channel_id, 'limit': '1000', 'oldest': '0'}
        thread_list = get_thread_list(headers, params)

        save_message_path = os.path.join(channel_name, f'{channel_name}_message.json')
        dump_json(thread_list, save_message_path)
        download_files(channel_name, thread_list)

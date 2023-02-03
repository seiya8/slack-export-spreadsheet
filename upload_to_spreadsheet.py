import csv
import json
import os
import sys
import time

import gspread
from gspread_formatting import set_column_widths
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

class DriveUploader:
    def __init__(self, credentials):
        self.gauth = GoogleAuth()
        self.gauth.credentials = credentials
        self.drive = GoogleDrive(self.gauth)

    def create_file(self, parents_id, file_name, mimeType):
        file_metadata = {
            'title': file_name,
            'parents': [{'id': parents_id}],
            'mimeType': mimeType
        }
        time.sleep(1)
        folder = self.drive.CreateFile(file_metadata)
        folder.Upload()
        return folder['id']

    def upload_file(self, parents_id, file_path):
        file_metadata = {
            'title': file_path.split('/')[-1],
            'parents': [{'id': parents_id}],
        }
        time.sleep(1)
        file = self.drive.CreateFile(file_metadata)
        file.SetContentFile(file_path)
        file.Upload()
        return file['id']

    def upload_profile_images(self):
        file_id_dict = {}
        profile_image_folder_id = self.create_file(folder_id, 'profile_images', 'application/vnd.google-apps.folder')
        for filename in os.listdir('output/profile_images'):
            file_path = f'output/profile_images/{filename}'
            file_id = self.upload_file(profile_image_folder_id, file_path)
            file_id_dict[filename.split('.')[0]] = file_id
        return file_id_dict

if __name__ == '__main__':
    json_file = sys.argv[1]
    folder_id = sys.argv[2]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
    uploader = DriveUploader(credentials)

    profile_image_id_dict = uploader.upload_profile_images()

    with open('channels.json', 'r') as f:
        channel_dict = json.load(f)

    sh_id = uploader.create_file(folder_id, 'posts', 'application/vnd.google-apps.spreadsheet')
    gc = gspread.authorize(credentials)
    sh_url = f'https://docs.google.com/spreadsheets/d/{sh_id}'
    sh = gc.open_by_url(sh_url)

    for channel_name in channel_dict.values():
        print(f'channel: {channel_name}')
        ws = sh.add_worksheet(title=channel_name, rows=2000, cols=26)

        set_column_widths(ws, [('A', 120), ('B', 20), ('C', 120), ('D', 550), ('E', 550), ('F', 300)])
        ws.format('A:F', {'wrapStrategy': 'WRAP', 'verticalAlignment': 'TOP'})

        time.sleep(1)
        channel_folder_id = uploader.create_file(folder_id, channel_name, 'application/vnd.google-apps.folder')
        with open(f'output/csv_files/{channel_name}.csv') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                profile_image_id = profile_image_id_dict[row[1]]
                row[1] = f'=IMAGE("https://drive.google.com/uc?export=download&id={profile_image_id}", 4, 20, 20)'
                if row[5]:
                    ts = row[5].split('/')[-2]
                    subfolder_id = uploader.create_file(channel_folder_id, ts, 'application/vnd.google-apps.folder')

                    time.sleep(1)
                    file_id = uploader.upload_file(subfolder_id, row[5])
                    file_name = row[5].split('/')[-1]
                    row[5] = f'=HYPERLINK("https://drive.google.com/file/d/{file_id}", "{file_name}")'

                cell_list = ws.range(i+1, 1, i+1, 6)
                for j, v in enumerate(row):
                    cell_list[j].value = v

                time.sleep(1)
                ws.update_cells(cell_list, value_input_option='USER_ENTERED')
    sh.del_worksheet(sh.worksheet('Sheet1'))

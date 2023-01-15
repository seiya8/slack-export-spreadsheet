import json
import sys
import time

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


class DriveUploader:
    def __init__(self, json_file):
        self.gauth = GoogleAuth()
        self.gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, ["https://www.googleapis.com/auth/drive"])
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
        
    def upload_file(self, parents_id, file_path):
        file_metadata = {
            'title': file_path,
            'parents': [{'id': parents_id}],
        }
        time.sleep(1)
        file = self.drive.CreateFile(file_metadata)
        file.SetContentFile(file_path)
        file.Upload()
        print(file['id'])

if __name__ == '__main__':
    json_file = sys.argv[1]
    folder_id = sys.argv[2]

    uploader = DriveUploader(json_file)
    uploader.create_file(folder_id, 'message', 'application/vnd.google-apps.spreadsheet')

    with open('channels.json', 'r') as f:
        channel_dict = json.load(f)

    for channel_name in channel_dict.values():
        uploader.create_file(folder_id, channel_name, 'application/vnd.google-apps.folder')

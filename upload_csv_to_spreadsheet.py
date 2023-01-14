import csv
import json
import sys
import time

from google.oauth2.service_account import Credentials
import gspread
from gspread_formatting import set_column_width

credentials = Credentials.from_service_account_file(
    'civil-sentry-374604-45bb122ed1a1.json',
    scopes= ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)

gc = gspread.authorize(credentials)
sh = gc.open_by_url(sys.argv[1])

with open('channels.json', 'r') as f:
    channel_dict = json.load(f)
    
for channel_name in channel_dict.values():
    ws = sh.add_worksheet(title=channel_name, rows=1000, cols=26)
    
    set_column_width(ws, 'A', 120)
    set_column_width(ws, 'B', 120)
    set_column_width(ws, 'C', 600)
    set_column_width(ws, 'D', 300)
    set_column_width(ws, 'E', 600)
    ws.format('A:E', {'wrapStrategy': 'WRAP', 'verticalAlignment': 'TOP'})
    
    with open(f'output/csv_files/{channel_name}.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            cell_list = ws.range(i+1, 1, i+1, 5)
            for j, v in enumerate(row):
                cell_list[j].value = v
                
            time.sleep(1)
            ws.update_cells(cell_list)

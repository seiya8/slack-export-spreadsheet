#!/bin/bash
read -p "token: " TOKEN
read -p "json file: " JSON_FILE
read -p "folder id: " FOLDER_ID
if [ ! -e $JSON_FILE ]; then
    echo "JSON file does not exist" 1>&2
    exit 1
fi
echo 'exporting slack data'
echo '----'
python export_slack_data.py $TOKEN
echo '----'
echo 'uploading data to spreadsheet'
echo '----'
python upload_to_spreadsheet.py $JSON_FILE $FOLDER_ID
echo 'done!'
#!/bin/bash
SLACK_USER_TOKEN=
JSON_FILE=
FOLDER_ID=
SLACK_BOT_TOKEN=
CHANNEL_ID=

if [ ! -e $JSON_FILE ]; then
    echo "JSON file does not exist" 1>&2
    exit 1
fi
echo 'exporting slack data'
echo '----'
python export_slack_data.py $SLACK_USER_TOKEN
echo '----'
echo 'uploading data to spreadsheet'
echo '----'
python upload_to_spreadsheet.py $JSON_FILE $FOLDER_ID $SLACK_BOT_TOKEN $CHANNEL_ID
echo 'done!'

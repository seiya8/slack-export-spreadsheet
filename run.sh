echo 'exporting slack data'
echo '----'
python export_slack_data.py $1
echo '----'
echo 'uploading data to spreadsheet'
echo '----'
python upload_to_spreadsheet.py $2 $3
echo 'done!'

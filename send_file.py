import requests
import glob
import time
import os


path = "/root/connector-alienvault"

def send_to_telegram(file_path):
    API_TOKEN = "5605337138:AAFtoMEMSmfUD0Sq0zb3LORQE2q-HZuBvgY"
    CHANNEL_ID = "-849383379"
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendDocument"
    
    files = {'document': (file_path, open(file_path, 'rb'))}
    data = {'chat_id': CHANNEL_ID}
    
    response = requests.post(url, files=files, data=data)
    
    return response.json()

def send_new_json_files(path, API_TOKEN, CHANNEL_ID):
    while True:
        files = glob.glob(f"{path}/*.json")
        for file in files:
            send_to_telegram(file, API_TOKEN, CHANNEL_ID)
            print("send")
            os.remove(file)
            print("remove")
            
        
        time.sleep(5) # sleep for 60 seconds before checking for new files again

send_new_json_files(path, API_TOKEN, CHANNEL_ID)
import requests
import os
from dotenv import load_dotenv

load_dotenv()
def send_line_notify(message):
    line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
    
    if line_notify_token == "":
        return "Please set LINE Notify token"
    
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }
    data = {
        "message": message
    }
    # data is form-data
    response = requests.post(line_notify_api, headers=headers, data=data)
    print(f"[notification.send_line_notify] response: {response.text}")
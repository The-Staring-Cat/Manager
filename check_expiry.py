import os
import requests
from datetime import datetime

# CONFIG - These will be stored in GitHub Secrets
SB_URL = os.getenv('SB_URL')
SB_KEY = os.getenv('SB_KEY')
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def check_clients():
    # Fetch clients from Supabase
    headers = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}"}
    response = requests.get(f"{SB_URL}/rest/v1/clients", headers=headers)
    clients = response.json()

    today = datetime.now().date()

    for c in clients:
        expiry_date = datetime.strptime(c['expiry_date'], '%Y-%m-%d').date()
        days_left = (expiry_date - today).days

        msg = ""
        if days_left == 2:
            msg = f"⚠️ <b>2 DAYS LEFT</b>\nClient: {c['name']}\nService: {c['service_name']}"
        elif days_left == 1:
            msg = f"🚨 <b>1 DAY LEFT</b>\nClient: {c['name']}\nService: {c['service_name']}"
        elif days_left == 0:
            msg = f"❌ <b>EXPIRED TODAY</b>\nClient: {c['name']}\nService: {c['service_name']}"
        elif days_left == -1:
            msg = f"💀 <b>EXPIRED YESTERDAY</b>\nClient: {c['name']}\n(Final Warning)"

        if msg:
            send_telegram(msg)

if __name__ == "__main__":
    check_clients()

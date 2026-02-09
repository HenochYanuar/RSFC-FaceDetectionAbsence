import requests
from django.conf import settings

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)
    return response.json()

def send_telegram_message_hrd(hrd_list, message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    for hrd in hrd_list:
      payload = {
          "chat_id": hrd.telegram_chat_id,
          "text": message,
          "parse_mode": "HTML"
      }

      response = requests.post(url, data=payload)
    return response.json()
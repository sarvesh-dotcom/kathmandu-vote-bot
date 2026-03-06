import requests
import time

BOT_TOKEN = "8716448487:AAHiQmGr1sPugDfdKTJ3jKZuF8m6ThY5BiU"
CHAT_ID = "-430883755"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def main():
    print("🚀 railway bot started")
    send_message("✅ Railway Telegram bot is running")
    print("message sent")
    time.sleep(999999)  # keep container alive

if __name__ == "__main__":
    main()
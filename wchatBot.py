import socketio, os
#import google.generativeai as genai
from requests import post
from datetime import datetime

# 創建 SocketIO 客戶端
sio = socketio.Client()

options = {
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": prompt
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 1,
    "topK": 40,
    "topP": 0.95,
    "maxOutputTokens": 900,
    "responseMimeType": "text/plain"
  }
}

# 當連接成功時的回調函數
@sio.event
def connect():
    print("Connected to the server")
    sio.emit('joinChat', { "username": "nelson", "room_number": "wbank客服" });

# 當接收到 'chatMessage' 事件時的回調函數
@sio.on('chatMessage')
def on_chat_message(data):
    if data["type"] == "text":
        if data["text"] in "H" or data["text"] in "h" or data["text"] in "你好":
            sio.emit("chatMessage",{ "username": "nelson", "type":"text", "text":"您好，請問有什麼可以幫忙？", "room_number": "wbank客服", "timestamp": datetime.now()});
        else:
            resp = post(url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-thinking-exp-01-21:generateContent?key={os.environ.get('gkey')}", headers={"Content-Type":"application/json"}, json=options)
            resp.raise_for_status()
            try:
              sio.emit("chatMessage",{ "username": "nelson", "type":"text", "text":resp.json()["candidates"][0]["content"]["parts"][0]["text"], "room_number": "wbank客服" , "timestamp": datetime.now()});
            except:
              sio.emit("chatMessage",{ "username": "nelson", "type":"text", "text":resp.json(), "room_number": "wbank客服" , "timestamp": datetime.now()});

# 當斷開連接時的回調函數
@sio.event
def disconnect():
    print("Disconnected from the server")
    sio.emit('leaveChat', { "username": "funGPT", "room_number": "wbank客服" });

def run_model():
  # 連接到 Socket.IO 伺服器
  sio.connect('https://sites.wtechhk.xyz')

  # 保持程序運行以接收消息
  sio.wait()
from flask import Flask, request, jsonify
import requests
import random
import os

app = Flask(__name__)

TOKEN = "447107892283877624:oedSMfxhfckBEqlvlEiGvrIVJbLxWHOppZmApWCoNeyKYKqwuVMHPWpTMiotWUpS"
API_URL = f"https://bot.zapps.me/api/v1/bot{TOKEN}/sendMessage" 

danh_sach_thanh_vien = ["Duy", "Thắng", "Nam", "An"]
thong_ke_tin_nhan = {"Duy": 150, "Thắng": 12, "Nam": 85, "An": 40}

def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    print(f"[BOT] Đang gửi tin nhắn tới {chat_id}: {text}")
    try:
        res = requests.post(API_URL, json=payload)
        print(f"[ZALO RESPONSE] Mã lỗi API: {res.status_code} - Phản hồi: {res.text}")
    except Exception as e:
        print(f"[ERROR] Lỗi kết nối API: {e}")

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Bot Sky Dodge đang hoạt động bình thường!", 200

    data = request.json
    print("\n=== [LOGS] DỮ LIỆU ZALO BẮN SANG WEBHOOK ===")
    print(data)
    print("=============================================\n")

    if not data:
        return jsonify({"status": "error"}), 400

    message = data.get("message", {})
    chat_id = None
    text = ""

    # Bóc tách linh hoạt để tránh lỗi cấu trúc
    if isinstance(data, dict):
        chat_id = data.get("group_id") or data.get("sender", {}).get("id")
        if isinstance(message, dict):
            text = str(message.get("text", "")).strip()
            chat_id = chat_id or message.get("chat_id") or message.get("chat", {}).get("id")
        else:
            text = str(data.get("text", "")).strip()

    if not chat_id:
        chat_id = "unknown"

    event_type = data.get("event_type") or (message.get("event_type") if isinstance(message, dict) else "chat")
    
    if event_type == "member_join":
        send_message(chat_id, "Chào thành viên mới.")
    elif event_type == "member_leave":
        send_message(chat_id, "Tạm biệt khi ai đó rời nhóm.")
    elif text == "/start":
        send_message(chat_id, "Xin chào, tôi là chat bot của nhóm Sky Dodge, tôi sẽ giải thích một số thông tin hữu ích về nhóm cho bạn.")
    elif text == "/parky":
        send_message(chat_id, "Theo tôi được biết Thắng là 1 con chó súc vật, chỉ biết cong đuôi khi anh em khó khăn, nên hạn chế tiếp xúc với người này.")
    elif text == "/asuna":
        send_message(chat_id, "Gửi bạn hình Asuna ngẫu nhiên: https://example.com/asuna_random.jpg")
    elif text == "/game":
        send_message(chat_id, "Link các web của Duy:\n- War Between Kings: [link]\n- Angry Fat - Random Map Edition: [link]")
    elif text == "/random":
        nguoi = random.choice(danh_sach_thanh_vien)
        send_message(chat_id, f"Người ngẫu nhiên được chọn là: {nguoi}")
    elif text == "/chain":
        send_message(chat_id, "Thống kê chuỗi nhắn tin của nhóm: Đang duy trì chuỗi 7 ngày liên tiếp.")
    elif text.startswith("/statistical"):
        parts = text.split(" ", 1)
        if len(parts) > 1:
            ten = parts[1]
            so_tin = thong_ke_tin_nhan.get(ten, 0)
            send_message(chat_id, f"Thống kê: {ten} đã gửi {so_tin} tin nhắn.")
        else:
            send_message(chat_id, "Vui lòng nhập tên. Ví dụ: /statistical Duy")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

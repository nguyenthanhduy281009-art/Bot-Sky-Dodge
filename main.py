from flask import Flask, request, jsonify
import requests
import random

app = Flask(name)

Thay mã Token thật của bạn vào đây
TOKEN = "447107892283877624:oedSMfxhfckBEqlvlEiGvrIVJbLxWHOppZmApWCoNeyKYKqwuVMHPWpTMiotWUpS"
API_URL = f"https://bot.zapps.me/api/v1/bot{TOKEN}"

danh_sach_thanh_vien = ["Duy", "Thắng", "Nam", "An"]
thong_ke_tin_nhan = {"Duy": 150, "Thắng": 12, "Nam": 85, "An": 40}

def send_message(chat_id, text):
requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route('/', methods=['POST'])
def webhook():
data = request.json
if not data:
return jsonify({"status": "error"}), 400

# Nhận dữ liệu tin nhắn từ Zalo gửi sang
message = data.get("message", {})
chat_id = message.get("chat", {}).get("id")
text = str(message.get("text", "")).strip()
event_type = message.get("event_type", "chat")

if not chat_id:
return jsonify({"status": "ok"}), 200

# 1. Xử lý các sự kiện tự động
if event_type == "member_join":
send_message(chat_id, "Chào thành viên mới.")
elif event_type == "member_leave":
send_message(chat_id, "Tạm biệt khi ai đó rời nhóm.")

# 2. Xử lý lệnh từ người dùng
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

if name == "main":
# Render yêu cầu chạy trên port 10000 hoặc port hệ thống cấp
app.run(host="0.0.0.0", port=10000)


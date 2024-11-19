from flask import request, jsonify
import json
import websocket
import dotenv
import os
import uuid
from utils.comfyui_utils import get_images

dotenv.load_dotenv()
comfy_ui_domain = os.getenv("COMFY_UI_DOMAIN")
client_id = str(uuid.uuid4())
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}
host = os.getenv("HOST")
# confyUIserverにpromptを送信し、imageを取得するcontroller

def post():
    # リクエストヘッダのContent-Lengthを取得
    content_length = int(request.headers['Content-Length'])

    # リクエストボディからデータを取得
    post_data = request.data
    json_data = json.loads(post_data)

    # websocketでserver_addressに接続し、imagesを返す
    ws = websocket.WebSocket()
    ws_url = "wss://{}/ws?clientId={}".format(comfy_ui_domain, client_id)

    try:
        ws = websocket.create_connection(ws_url)
        print("WebSocket connection established successfully.")
    except websocket.WebSocketException as e:
        print(f"WebSocket connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            images = get_images(ws, json_data)
            ws.close()

            # imageをoutputImagesディレクトリに保存
            for node, images in images.items():
                for i, image in enumerate(images):
                    with open(f"output/{node}_{client_id}.png", "wb") as f:
                        f.write(image)
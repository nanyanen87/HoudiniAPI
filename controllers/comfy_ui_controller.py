from flask import request, jsonify
import json
import websocket
import dotenv
import os
import sys
import uuid

dotenv.load_dotenv()
server_address_ws = os.getenv("CONFY_UI_SERVER_ADDRESS_WS")
client_id = str(uuid.uuid4())

host = os.getenv("HOST")
# confyUIserverにpromptを送信し、imageを取得するcontroller
def get():
    # リクエストヘッダのContent-Lengthを取得
    content_length = int(request.headers['Content-Length'])

    # リクエストボディからデータを取得
    post_data = request.data
    json_data = json.loads(post_data)
    print("Received JSON data:", json_data)  # コンソールに表示

    # websocketでserver_addressに接続し、imagesを返す
    ws = websocket.WebSocket()
    ws_url = "ws://{}/ws?clientId={}".format(server_address_ws, client_id)
    print(f"Connecting to {ws_url}")
    try:
        ws = websocket.create_connection(ws_url)
        print("WebSocket connection established successfully.")
    except websocket.WebSocketException as e:
        print(f"WebSocket connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ws' in locals() and ws.connected:
            images = self.get_images(ws, json_data)
            ws.close()

            # imageをoutputImagesディレクトリに保存
            for node, images in images.items():
                for i, image in enumerate(images):
                    with open(f"output/{node}_{client_id}.png", "wb") as f:
                        f.write(image)
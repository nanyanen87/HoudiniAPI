import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, parse
from dotenv import load_dotenv
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import sys
import os


load_dotenv()
host = os.getenv("HOST")
port = int(os.getenv("PORT"))
client_id = str(uuid.uuid4())
server_address = os.getenv("CONFY_UI_SERVER_ADDRESS")

class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # アクセスがあったことをコンソールに表示
        print(f"GET request received from {self.client_address[0]}:{self.client_address[1]}, Path: {self.path}")

        # 200 OKのレスポンスを返す
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"GET request received")

    def do_POST(self):
        # リクエストヘッダのContent-Lengthを取得
        content_length = int(self.headers['Content-Length'])

        # リクエストボディからデータを取得
        post_data = self.rfile.read(content_length)
        # todo 本来はこのjsonデータを使ってhdaを書き換える。

        # hapiでhdaを実行する
        try:

            # todo hdaがないのでとりあえずもらったpromptで実行
            json_data = json.loads(post_data)
            print("Received JSON data:", json_data)  # コンソールに表示


            # websocketでserver_addressに接続し、imagesを返す
            ws = websocket.WebSocket()
            ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
            images = self.get_images(ws, json_data)
            ws.close()
            # imageをoutputImagesディレクトリに保存
            for node, images in images.items():
                for i, image in enumerate(images):
                    with open(f"output/{node}_{i}.png", "wb") as f:
                        f.write(image)


        except json.JSONDecodeError:
            # JSONパースに失敗した場合のエラーハンドリング
            print("Invalid JSON format")
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'error', 'message': 'Invalid JSON format'}
            self.wfile.write(json.dumps(response).encode('utf-8'))


    def _queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req =  request.Request("http://{}/prompt".format(server_address), data=data)
        return json.loads(request.urlopen(req).read())

    def get_image(filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = parse.urlencode(data)
        with request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
            return response.read()

    def get_images(self, ws, prompt):
        prompt_id = self._queue_prompt(prompt)['prompt_id']
        output_images = {}
        current_node = ""
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['prompt_id'] == prompt_id:
                        if data['node'] is None:
                            break #Execution is done
                        else:
                            current_node = data['node']
            else: # 処理結果の画像データ
                if current_node == 'save_image_websocket_node':
                    images_output = output_images.get(current_node, [])
                    images_output.append(out[8:])
                    output_images[current_node] = images_output

        return output_images



# カスタムハンドラーとサーバーの作成
server = HTTPServer((host, port), CustomHandler)

print(f"Server started at http://{host}:{port}")
server.serve_forever()


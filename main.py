import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, parse
from dotenv import load_dotenv
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import sys
import os
# 通っているpathをすべて表示

# sys.path.append(r"C:\Program Files\Side Effects Software\Houdini 20.5.388\bin\LibHAPIL.dll")
# sys.path.append(r"C:\Program Files\Side Effects Software\Houdini 20.5.388\bin\LibHAPI.dll")
# sys.path.append(r"C:\Program Files\Side Effects Software\Houdini 20.5.388\custom\houdini\dsolib\libHAPIL.lib")
# sys.path.append(r"C:\Program Files\Side Effects Software\Houdini 20.5.388\custom\houdini\dsolib\libHAPI.lib")
# sys.path.append(r"C:\Program Files\Side Effects Software\Houdini 20.5.388\toolkit\include\HAPI")

# windowsで設定してもなぜか通らないのでpythonから設定\
houdini_bin_path = r"C:\Program Files\Side Effects Software\Houdini 20.5.388\bin"
os.add_dll_directory(houdini_bin_path)

# 環境変数を読み込む
load_dotenv()
houdini_bin_path = os.getenv("HOUDINI_BIN_PATH")
houdini_python_lib_path = os.getenv("HOUDINI_PYTHON_LIB_PATH")

server_address = os.getenv("CONFY_UI_SERVER_ADDRESS")
host = os.getenv("HOST")
port = int(os.getenv("PORT"))
sys.path.append(houdini_python_lib_path)

import hapi
import hou


# server_address = "http://172.17.92.170:50001/"
client_id = str(uuid.uuid4())

# HARSを起動
hars_host = os.getenv("HARS_HOST")
hars_port = int(os.getenv("HARS_PORT"))
log_path = "houdini.log"
options = hapi.ThriftServerOptions()
process_id = hapi.startThriftSocketServer(options, hars_port, log_path)

print(f"Thrift server started with process ID: {process_id}")

# セッション情報を作成
session_info = hapi.SessionInfo()
session = hapi.createThriftSocketSession(hars_host, hars_port, session_info)
cook_options = hapi.CookOptions()

# すでにセッションが初期化されている場合はcontinue
try:
    hapi.isInitialized(session)
    print("Session already initialized.")
except hapi.NotInitializedError:
    hapi.initialize(session, cook_options)
    print("Session initialized.")


try:
    print("In-Process session created successfully!")
    node_id = hapi.createNode(session, -1, 'Sop/curve')
    node_id2 = hapi.createNode(session, -1, 'Sop/grid')
    # その新しいノードのhapi.NodeInfoを取得します。


    node_info = hapi.getNodeInfo(session, node_id)
    # 文字列を取得するために2つの手順を踏みます。
    str_len = hapi.getStringBufLength(session, node_info.nameSH)
    node_name = hapi.getString(session, node_info.nameSH, str_len)
    print(f"Created node: {node_name}")


    # fileを保存
    hapi.saveHIPFile(session, "output" + "\\" + "{}.hip".format(node_name), True)
    hapi.cleanup(session)
    hapi.closeSession(session)
except hapi.FailureError as e:
    print(f"FailureError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


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


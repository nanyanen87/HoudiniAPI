# Flaskでhoudini操作用のサーバーを立てる
# 将来的にはこのファイルをmain.pyにして、endpointで起動、停止、実行を行う
# endpointは/start_hars, /stop_hars, /executeの３つ
# sessionをcloseせずにサーバーを終了させると、PORTが開放されないので、次回サーバーを立てるときにエラーが出る
from flask import Flask, jsonify
import os
import socket
import sys
from dotenv import load_dotenv


load_dotenv()
HOUDINI_BIN_PATH = os.getenv("HOUDINI_BIN_PATH")
HOUDINI_PYTHON_LIB_PATH = os.getenv("HOUDINI_PYTHON_LIB_PATH")
HARS_PORT = int(os.getenv("HARS_PORT"))
HARS_HOST = os.getenv("HARS_HOST")
APP_PORT = int(os.getenv("PORT"))
APP_HOST = os.getenv("HOST")
sys.path.append(HOUDINI_PYTHON_LIB_PATH)
os.add_dll_directory(HOUDINI_BIN_PATH)

app = Flask(__name__)
from controllers.start_hars_controller import start_hars
from controllers.stop_hars_controller import stop_hars
from controllers.execute_controller import execute
from controllers.execute_hda_controller import execute_hda

app.add_url_rule('/start_hars', view_func=start_hars, methods=['GET'])
app.add_url_rule('/stop_hars', view_func=stop_hars, methods=['GET'])
app.add_url_rule('/execute', view_func=execute, methods=['GET'])
app.add_url_rule('/execute_hda', view_func=execute_hda, methods=['GET'])

@app.route('/')
def index():
    # hello worldを返す
    return "Hello, World!"

# portが使用されているか確認
def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def main():
    # PORTが使用されているか確認
    if check_port(APP_PORT):
        # netstatでHARSのポートを使用しているプロセスを確認、それを止める
        #netstat -ano | findstr :9090
        #TCP         0.0.0.0:9090           0.0.0.0:0              LISTENING       3064
        #TCP         [::]:9090              [::]:0                 LISTENING       3064
        print(f"Port {APP_PORT} is already in use. タスクマネージャーからHARSを終了してください。")
        return
    app.run(host=APP_HOST, port=APP_PORT, debug=True)

if __name__ == "__main__":
    main()


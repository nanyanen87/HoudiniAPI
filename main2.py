# Flaskでhoudini操作用のサーバーを立てる
# 将来的にはこのファイルをmain.pyにして、endpointで起動、停止、実行を行う
# endpointは/start_hars, /stop_hars, /executeの３つ
# sessionをcloseせずにサーバーを終了させると、PORTが開放されないので、次回サーバーを立てるときにエラーが出る
import subprocess

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

# portが使用されていればTrueを返す
def is_port_in_use(port):
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
    return f":{port}" in result.stdout

def main():
    # PORTが使用されているか確認
    # debugモードならcheckしない。
    is_debug = True
    if not is_debug and is_port_in_use(HARS_PORT):
        print(f"Port {HARS_PORT} is already in use")
        return

    app.run(host=APP_HOST, port=APP_PORT, debug=is_debug)

if __name__ == "__main__":
    main()


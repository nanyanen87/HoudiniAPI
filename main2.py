# Flaskでhoudini操作用のサーバーを立てる
# 将来的にはこのファイルをmain.pyにして、endpointで起動、停止、実行を行う
# endpointは/start_hars, /stop_hars, /executeの３つ
# sessionをcloseせずにサーバーを終了させると、PORTが開放されないので、次回サーバーを立てるときにエラーが出る
import subprocess

from flask import Flask, jsonify
import os
import socket
import sys
import pkgutil
import importlib
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

from controllers import register_controllers

@app.route('/')
def index():
    # hello worldを返す
    return "Hello, World!"

# portが使用されていればTrueを返す
def is_port_in_use(port):
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
    return f":{port}" in result.stdout

def main():
    # controllerの初期化
    register_controllers(app)

    # PORTが使用されているか確認
    # debugモードならcheckしない。
    is_debug = True
    if not is_debug and is_port_in_use(HARS_PORT):
        print(f"Port {HARS_PORT} is already in use")
        return

    app.run(host=APP_HOST, port=APP_PORT, debug=is_debug)


if __name__ == "__main__":
    main()


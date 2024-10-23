# Flaskでhoudini操作用のサーバーを立てる
# 将来的にはこのファイルをmain.pyにして、endpointで起動、停止、実行を行う
# endpointは/start_hars, /stop_hars, /executeの３つ
from flask import Flask, jsonify
import os
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
import hapi

app = Flask(__name__)
from controllers.start_hars_controller import start_hars
from controllers.stop_hars_controller import stop_hars
from controllers.execute_controller import execute

app.add_url_rule('/start_hars', view_func=start_hars, methods=['GET'])
app.add_url_rule('/stop_hars', view_func=stop_hars, methods=['GET'])
app.add_url_rule('/execute', view_func=execute, methods=['GET'])

@app.route('/')
def index():
    # hello worldを返す
    return "Hello, World!"

# @app.route('/start_hars', methods=['GET'])
# def start_hars():
#
#     # hars_process_idがある場合は、すでに起動しているのでエラーを返す
#     if 'hars_process_id' in globals():
#         return jsonify({"error": "HARS server is already running"}), 400
#
#     today = datetime.date.today()
#     try:
#         options = hapi.ThriftServerOptions()
#         options.autoClose = False
#         options.timeoutMs = 10000
#         log_path = "houdini-" + today.strftime("%Y%m%d") + ".log"
#         process_id = hapi.startThriftSocketServer(options, HARS_PORT, log_path)
#     except hapi.FailureError as e:
#         print(f"FailureError: {e}")
#         return jsonify({"error": f"FailureError: {e}"}), 500
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": f"An error occurred: {e}"}), 500
#
#     # process_idをglobal変数にしておいて、stop_harsで使う
#     global hars_process_id
#     hars_process_id = process_id
#
#     print(f"Thrift server started with process ID: {process_id}")
#     return jsonify({"message": f"Thrift server started with process ID: {process_id}"}), 200

# @app.route('/stop_hars', methods=['GET'])
# def stop_hars():
#     # hars_process_idがない場合は、HARS serverが起動していないのでエラーを返す
#     if 'hars_process_id' not in globals():
#         return jsonify({"error": "HARS server is not running"}), 400
#
#     # processが存在するか確認
#     if check_process(hars_process_id):
#         kill_process(hars_process_id)
#     else:
#         print(f"Process {hars_process_id} is not running.")
#     return jsonify({"message": "HARS server stopped successfully"}), 200

# @app.route('/execute', methods=['POST'])
# def execute():
#     session = init_hars_session()
#     try:
#         create_node()
#         node_id = hapi.createNode(session, -1, 'Sop/curve')
#         node_id2 = hapi.createNode(session, -1, 'Sop/grid')
#         node_info = hapi.getNodeInfo(session, node_id)
#         str_len = hapi.getStringBufLength(session, node_info.nameSH)
#         node_name = hapi.getString(session, node_info.nameSH, str_len)
#         print(f"Created node: {node_name}")
#         today = datetime.date.today()
#
#         hapi.saveHIPFile(session, "output" + today.strftime("%Y%m%d") + "\\" + "{}.hip".format(node_name), True)
#         hapi.cleanup(session)
#         hapi.shutdown(session)
#         hapi.closeSession(session)
#     except hapi.FailureError as e:
#         print(f"FailureError: {e}")
#         return jsonify({"error": f"FailureError: {e}"}), 500
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": f"An error occurred: {e}"}), 500
#     return jsonify({"message": "Node created successfully"}), 200

print("server started")
if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=True)




# 接続確立用と作業用のsessionを分ける
def init_hars_session():
    # server通信確立sessionと作業用のsessionはわける？
    sys.path.append(HOUDINI_PYTHON_LIB_PATH)
    session_info = hapi.SessionInfo()
    session = hapi.createThriftSocketSession(HARS_HOST, HARS_PORT, session_info)
    cook_options = hapi.CookOptions()

    try:
        hapi.isInitialized(session)
        print("Session already initialized.")
    except hapi.NotInitializedError:
        hapi.initialize(session, cook_options)
        print("Session initialized.")
    return session


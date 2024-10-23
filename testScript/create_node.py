from dotenv import load_dotenv
import uuid
import sys
import os

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


# # HARSを起動
hars_host = os.getenv("HARS_HOST")
hars_port = int(os.getenv("HARS_PORT"))


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


# websocketで接続するためのclient_idを生成
client_id = str(uuid.uuid4())

try:
    print("In-Process session created successfully!")

    # hapiの処理
    create_node()
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
    hapi.shutdown(session)
    hapi.closeSession(session)
except hapi.FailureError as e:
    print(f"FailureError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")



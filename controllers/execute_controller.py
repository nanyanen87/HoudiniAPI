import datetime
from flask import jsonify
import sys
import hapi
from config import HARS_PORT, HARS_HOST, HOUDINI_PYTHON_LIB_PATH

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

def execute():
    session = init_hars_session()
    try:
        node_id = hapi.createNode(session, -1, 'Sop/curve')
        node_info = hapi.getNodeInfo(session, node_id)
        str_len = hapi.getStringBufLength(session, node_info.nameSH)
        node_name = hapi.getString(session, node_info.nameSH, str_len)
        print(f"Created node: {node_name}")
        today = datetime.date.today()

        output_path = "output"
        # file名を日付+ノード名にする
        file_name = f"{today.strftime('%Y%m%d')}_{node_name}.hip"
        hapi.saveHIPFile(session, f"{output_path}/{file_name}", True)
        hapi.cleanup(session)
        hapi.shutdown(session)
        hapi.closeSession(session)
    except hapi.FailureError as e:
        print(f"FailureError: {e}")
        return jsonify({"error": f"FailureError: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500
    return jsonify({"message": "Node created successfully"}), 200
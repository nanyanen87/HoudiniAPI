import datetime
from flask import jsonify
import hapi
import psutil
from config import HARS_PORT

def get(is_internal=False):

    # hars_process_idがある場合は、すでに起動しているのでエラーを返す
    if 'hars_process_id' in globals():
        return jsonify({"error": "HARS server is already running at process ID: {hars_process_id}"}), 400

    # HARS.exeがprocessの中にあるか確認
    for proc in psutil.process_iter():
        if proc.name() == "HARS.exe":
            return jsonify({"error": f"HARS server is already running at {proc.id}"}), 400


    today = datetime.date.today()
    options = hapi.ThriftServerOptions()
    options.autoClose = False
    options.timeoutMs = 10000
    log_path = "logs/houdini-" + today.strftime("%Y%m%d") + ".log"
    try:
        # logファイル作成
        open(log_path, "w").close()
        process_id = hapi.startThriftSocketServer(options, HARS_PORT, log_path)
    except hapi.FailureError as e:
        print(f"FailureError: {e}")
        return jsonify({"error": f"FailureError: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

    # process_idをglobal変数にしておいて、stop_harsで使う
    global hars_process_id
    hars_process_id = process_id

    print(f"Thrift server started with process ID: {process_id}")

    if is_internal:
        return process_id
    else:
        return jsonify({"message": f"Thrift server started with process ID: {process_id}"}), 200
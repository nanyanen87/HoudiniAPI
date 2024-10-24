import os
import signal
import psutil
from flask import jsonify, request

def check_process(process_id: int):
    try:
        os.kill(process_id, 0)
    except OSError:
        return False
    else:
        return True

def kill_process(pid: int):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process {pid} killed.")
    except OSError as e:
        print(f"Failed to kill process {pid}: {e}")

def get_process_info(process_id: int):
    try:
        # プロセスIDからプロセスを取得
        process = psutil.Process(process_id)

        # プロセスの情報を取得
        info = {
            "pid": process.pid,
            "name": process.name(),
            "status": process.status(),
            "create_time": process.create_time(),
            "cpu_usage": process.cpu_percent(interval=1.0),
            "memory_info": process.memory_info(),
            "exe": process.exe(),  # 実行ファイルのパス
            "cmdline": process.cmdline()  # コマンドライン引数
        }
        return info
    except psutil.NoSuchProcess:
        return f"Process with ID {process_id} does not exist."
    except psutil.AccessDenied:
        return f"Access denied to process with ID {process_id}."
    except Exception as e:
        return str(e)

# process_idを受け取りそれをkllする
def stop_hars():
    process_id = request.args.get("process_id")
    # process_idをintに変換
    process_id = int(process_id) if process_id else None
    if not process_id:
        return jsonify({"error": "process_id is required"}), 400

    print(f"Stopping process {process_id}...")
    process_info = get_process_info(process_id)

    print(f"Process info: {process_info}")
    # process nameが HARSdであるか確認
    if process_info["name"] != "HARS.exe":
        return jsonify({"error": "Invalid process ID"}), 400

    # kill
    kill_process(process_id)
    return jsonify({"message": f"Process {process_id} stopped successfully"}), 200


import os
from dotenv import load_dotenv
import sys
import datetime
# windowsで設定してもなぜか通らないのでpythonから設定\
houdini_bin_path = r"C:\Program Files\Side Effects Software\Houdini 20.5.388\bin"
os.add_dll_directory(houdini_bin_path)

# 環境変数を読み込む
load_dotenv()
houdini_bin_path = os.getenv("HOUDINI_BIN_PATH")
houdini_python_lib_path = os.getenv("HOUDINI_PYTHON_LIB_PATH")
sys.path.append(houdini_python_lib_path)
import hapi


# HARSを起動
hars_host = os.getenv("HARS_HOST")
hars_port = int(os.getenv("HARS_PORT"))
# 今日の日付
today = datetime.date.today()
log_path = "houdini-" + today.strftime("%Y%m%d") + ".log"
options = hapi.ThriftServerOptions()
options.autoClose = False
options.timeoutMs = 10000
# objectの中身を表示
print(options.autoClose)
print(options.timeoutMs)

session_info = hapi.SessionInfo()

try:
    process_id = hapi.startThriftSocketServer(options, hars_port, log_path)
except hapi.FailureError as e:
    print(f"FailureError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
print(f"Thrift server started with process ID: {process_id}")
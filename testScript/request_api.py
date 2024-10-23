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
hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\top_hanaoka_nan.apirequest.1.0.hdanc"

# セッション情報を作成
session_info = hapi.SessionInfo()
session = hapi.createThriftSocketSession(hars_host, hars_port, session_info)
cook_options = hapi.CookOptions()

# すでにセッションが初期化されている場合はcontinue
try:
    hapi.isInitialized(session)
    print("Session already initialized.")
except hapi.NotInitializedError:
    hapi.initialize(session, cook_options, otl_search_path=hda_path)
    print("Session initialized.")


# websocketで接続するためのclient_idを生成
client_id = str(uuid.uuid4())

print("In-Process session created successfully!")
try:

    # hdaを実行する
    my_library_id = hapi.loadAssetLibraryFromFile(session, hda_path, True)
    library_count = hapi.getLoadedAssetLibraryCount(session)
    library_ids = hapi.getAssetLibraryIds(session, 0, library_count)

    library_id = my_library_id
    # library_id = library_ids[2]
    asset_count = hapi.getAvailableAssetCount(session, library_id)
    library_path_id = hapi.getAssetLibraryFilePath(session, library_id)


    print(f"Loaded asset libraries: {library_ids}")
    id_list = hapi.getAvailableAssets(session, library_id, asset_count)
    try:
        # id_listの個数を取得




        for i in range(asset_count):
            print(f"Available asset: {id_list[i]}")


        # info = hapi.getAssetInfo(session, id_list[0])
        # print(f"Asset info: {info}")
        # id_list[0]をstringに変換
        operator_name = str(id_list[0])

        # asset nameとはなんぞや。他のassetから予想する必要がある。
        array = hapi.getAssetDefinitionParmCounts(session, id_list[0], '')
        print(f"Asset definition parm counts: {array}")

        # Sopなら作れているから状況が間違えてる
        # node_id = hapi.createNode(session, -1, operator_name)
        node_id = hapi.createNode(session, -1, 'Sop/curve')
        print(f"Type of node_id: {type(node_id)}")
        int_node_id = int(node_id)
        print(f"Created node: {int_node_id}")
        # その新しいノードのhapi.NodeInfoを取得します。
        asset_info = hapi.getAssetInfo(session, node_id)
        print(f"Asset info: {asset_info}")
        #
        #
        #
        #
        node_info = hapi.getNodeInfo(session, int_node_id)
        print(f"Node info: {node_info}")
        # 文字列を取得するために2つの手順を踏みます。
        str_len = hapi.getStringBufLength(session, node_info.nameSH)
        node_name = hapi.getString(session, node_info.nameSH, str_len)
        print(f"Created node: {node_name}")
    except hapi.FailureError as e:
        print(f"hapi cook failure: {e}")
    except Exception as e:
        print(f"normal FailureError: {e}")



    status_type = hapi.statusType.CallResult
    status_length = hapi.getStatusStringBufLength(session, status_type, hapi.statusVerbosity.All)
    status = hapi.getStatusString(session, status_type, status_length)
    print(f"Status: {status}")
    print(f"session_close execute: {library_path_id}")
    hapi.cleanup(session)
    hapi.shutdown(session)
    hapi.closeSession(session)
except hapi.FailureError as e:
    print(f"FailureError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

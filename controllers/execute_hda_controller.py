import datetime
from flask import jsonify
import sys
import hapi
from config import HARS_PORT, HARS_HOST, HOUDINI_PYTHON_LIB_PATH
hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\top_hanaoka_nan.apirequest.1.0.hdanc"

# 接続確立用と作業用のsessionを分ける
def init_hars_session():
    # server通信確立sessionと作業用のsessionはわける？
    sys.path.append(HOUDINI_PYTHON_LIB_PATH)
    session_info = hapi.SessionInfo()
    session = hapi.createInProcessSession(session_info)


    # session = hapi.createThriftSocketSession(HARS_HOST, HARS_PORT, session_info)
    cook_options = hapi.CookOptions()

    try:
        hapi.isInitialized(session)
        print("Session already initialized.")
    except hapi.NotInitializedError:
        hapi.initialize(session, cook_options, otl_search_path=hda_path)
        print("Session initialized.")
    return session

def execute_hda():
    session = init_hars_session()
    try:
        print("In-Process session created successfully!")

        # hdaを読み込む
        hda_bytes = open(hda_path, "rb").read()
        lib_id = hapi.loadAssetLibraryFromMemory(session, hda_bytes,len(hda_bytes), True)
        print(f"Loaded asset library id: {lib_id}")

        # asset libraryの中にあるassetを取得
        asset_count = hapi.getAvailableAssetCount(session, lib_id)
        print(f"Available asset count: {asset_count}")

        asset_name_sh_list = hapi.getAvailableAssets(session, lib_id, asset_count)
        # asset_nameを取得
        my_asset_name = ''
        for i in range(asset_count):
            asset_name_length = hapi.getStringBufLength(session, asset_name_sh_list[i])
            asset_name = hapi.getString(session, asset_name_sh_list[i], asset_name_length)
            # 一番最初のassetを取得
            if i == 0:
                my_asset_name = asset_name
            print(f"Available asset: {asset_name}")


        # libraryの中にあるassetを取得
        library_id_sh = hapi.getAssetLibraryFilePath(session, lib_id)
        path_name_length = hapi.getStringBufLength(session, library_id_sh)
        path_name = hapi.getString(session, library_id_sh, path_name_length)
        print(f"Loaded asset library path name: {path_name}")
        # my_asset_name = "hanaoka_nan::Top/apirequest::1.0"　だがoperator_nameには" hanaoka_nan::apirequest::1.0"が入る
        parent_node_id = hapi.createNode(session, -1, "Top/topnet")
        print(f"Parent node id: {parent_node_id}")
        node_id = hapi.createNode(session, parent_node_id, 'hanaoka_nan::apirequest::1.0')
        # node_id = hapi.createNode(session=session, parent_node_id=parent_node_id, operator_name=my_asset_name, node_label="apirequest", cook_on_creation=False)

        print(f"node id: {node_id}")
        print(f"node id type: {type(node_id)}")
        node_info = hapi.getNodeInfo(session=session, node_id=node_id)
        print(f"node info: {node_info}")
        str_len = hapi.getStringBufLength(session, node_info.nameSH)
        node_name = hapi.getString(session, node_info.nameSH, str_len)
        print(f"Created node: {node_name}")
        now = datetime.datetime.now()

        output_path = "output"
        # file名を日付+ノード名にする
        file_name = f"{now.strftime('%Y%m%d-%H%M%S')}_{node_name}.hip"
        hapi.saveHIPFile(session, f"{output_path}/{file_name}", True)



    except hapi.FailureError as e:
        print(f"FailureError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    hapi.cleanup(session)
    print("Session cleaned up.")
    # hapi.shutdown(session)
    # hapi.closeSession(session)
    return jsonify({"message": "Node created successfully"}), 200


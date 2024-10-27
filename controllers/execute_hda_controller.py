import datetime
from flask import jsonify
import sys
import hapi
from config import HARS_PORT, HARS_HOST, HOUDINI_PYTHON_LIB_PATH
from testScript.create_node import node_name

hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\top_hanaoka_nan.apirequest.1.0.hdanc"
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, close_session

# 接続確立用と作業用のsessionを分ける?
def execute_hda():
    session = init_hars_session()
    try:
        print("session created successfully!")

        # hdaを読み込む
        hda_bytes = open(hda_path, "rb").read()
        lib_id = hapi.loadAssetLibraryFromMemory(session, hda_bytes,len(hda_bytes), True)
        print(f"Loaded asset library id: {lib_id}")

        # 読み込まれているlibraryを取得
        library_name = get_library_name(session, lib_id)
        print(f"Loaded asset library name: {library_name}")
        asset_names = get_asset_names(session, lib_id)
        # asset_nameを取得
        my_asset_name = ''
        for asset_name in asset_names:
            print(f"Available asset: {asset_name}")
            if "apirequest" in asset_name:
                my_asset_name = asset_name
                break


        # nodeを作成
        # my_asset_name = "hanaoka_nan::Top/apirequest::1.0"　だがoperator_nameには" hanaoka_nan::apirequest::1.0"が入る
        parent_node_id = hapi.createNode(session, -1, "Top/topnet")
        print(f"Parent node id: {parent_node_id}")
        node_id = hapi.createNode(session, parent_node_id, 'hanaoka_nan::apirequest::1.0')
        # node_id = hapi.createNode(session=session, parent_node_id=parent_node_id, operator_name=my_asset_name, node_label="apirequest", cook_on_creation=False)

        # print(f"node id: {node_id}")
        # print(f"node id type: {type(node_id)}")
        # node_info = hapi.getNodeInfo(session=session, node_id=node_id)
        # print(f"node info: {node_info}")
        # str_len = hapi.getStringBufLength(session, node_info.nameSH)
        # node_name = hapi.getString(session, node_info.nameSH, str_len)
        node_name = get_node_name(session, node_id)
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
    hapi.closeSession(session)
    return jsonify({"message": "Node created successfully"}), 200


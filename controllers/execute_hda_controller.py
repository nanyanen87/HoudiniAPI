import datetime
from flask import jsonify
import sys
import hapi
from utils.hapi_utils import convert_asset_name_to_operator_name, get_param_name, set_multi_param

# hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\top_hanaoka_nan.apirequest.1.0.hdanc"
hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\sop_Natsumaru.chair.1.0.hdalc"
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, \
    close_session, convert_asset_name_to_operator_name


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

        #　目的のnodeを置く parent_nodeを作成
        parent_node_id = hapi.createNode(session, -1, "Object/geo")
        # parent_node_id = hapi.createNode(session, -1, "Top/topnet")

        # node作成
        # natsumaru node作成　Natsumaru::Sop/chair::1.0
        my_asset_name = get_asset_names(session, lib_id)[0]
        # asset_nameをoperator_nameに変換　Natsumaru::chair::1.0
        operator_name = convert_asset_name_to_operator_name(my_asset_name)
        node_id = hapi.createNode(session, parent_node_id, operator_name)
        node_name = get_node_name(session, node_id)
        print(f"Created node: {node_name}")

        # paramを取得
        node_info = hapi.getNodeInfo(session, node_id)
        node_info_param_count = node_info.parmCount
        param_info_list = hapi.getParameters(session, node_id, 0, node_info_param_count)
        for i in range(node_info_param_count):
            param_name = get_param_name(session, node_id, param_info_list[i].id)
            print(param_name)

        # paramを一気に設定
        # seat_height
        # back_height
        # width
        # depth
        # frame_size
        # cushion_depth
        # cushion_bevel
        set_multi_param(session, node_id, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])


        # 保存
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


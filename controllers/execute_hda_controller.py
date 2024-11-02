import datetime
from flask import jsonify
import sys
import hapi


# hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\top_hanaoka_nan.apirequest.1.0.hdanc"
# hda_path = r"C:\\Users\\hanaoka nan\\AppDevelop\\houdiniScript\\hdaFiles\\sop_Natsumaru.chair.1.0.hdalc"
hda_path = r"/input_files/object_tsuno.sample_pig_image_copy.1.0.hdanc"
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, \
    close_session, get_child_node_ids

#todo hdaからcreateしたnodeにはlockがかかっているので、解除する必要がある
def __generate_image_from_top_node(session, top_node_id):
    # top nodeをcookPDG
    node_name = get_node_name(session, top_node_id)
    # res = hapi.cookPDG(session, top_node_id, 0, 1)

    #　cookPDGAllOutputs,ropfetchのnode_idだと「 cook_node_id should be a TOP Network」エラーが出る
    res = hapi.cookPDGAllOutputs(session, top_node_id, 1, 1)
    print(f"Top node cooked: {node_name} {res}")
    context_id = hapi.getPDGGraphContextId(session, top_node_id)

    # graph_context_count = hapi.getPDGGraphContextsCount(session)
    # context_names_and_ids = hapi.getPDGGraphContexts(session, 0, graph_context_count)
    # for graph_context_sh in context_names_and_ids[0]:
    #     len = hapi.getStringBufLength(session, graph_context_sh)
    #     graph_context = hapi.getString(session, graph_context_sh, len)
    #     print(f"Graph context: {graph_context}")


    state_int = hapi.getPDGState(session, context_id)
    length = hapi.getStringBufLength(session,state_int)
    state = hapi.getString(session, state_int, length)
    print(f"Top node cooked: {node_name} {res} {state}")

def get():
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
        # parent_node_id = hapi.createNode(session, -1, "Object/geo")
        # parent_node_id = hapi.createNode(session, -1, "Top/topnet")

        # node作成
        # natsumaru node作成　Natsumaru::Sop/chair::1.0
        my_asset_name = get_asset_names(session, lib_id)[0]
        # asset_nameをoperator_nameに変換　Natsumaru::chair::1.0
        print(f"Operator name: {my_asset_name}")
        node_id = hapi.createNode(session, -1, my_asset_name)
        node_name = get_node_name(session, node_id)
        print(f"Created node: {node_name}")



        # object nodeを取得(childの下位互換っぽい)
        # obj_count = hapi.composeObjectList(session, node_id, None)
        # print(f"Object count: {obj_count}")
        # obj_info_list = hapi.getComposedObjectList(session, node_id, 0, obj_count)
        # for obj_info in obj_info_list:
        #     obj_node_id = obj_info.nodeId
        #     obj_name = get_node_name(session, obj_node_id)
        #     print(f"Object node: {obj_name}")


        #child node idを取得
        child_count = hapi.composeChildNodeList(session, node_id,hapi.nodeType.Any,hapi.nodeFlags.Any,False)
        print(f"Child count: {child_count}")
        child_node_ids = hapi.getComposedChildNodeList(session, node_id, child_count)
        print(f"Child node ids: {child_node_ids}")
        cook_options = hapi.CookOptions()
        for child_node_id in child_node_ids:
            node_name = get_node_name(session, child_node_id)
            print(f"Child node cooked: {node_name}")

        # __generate_image_from_top_node(session, 4)

        # grand_child_ids = get_child_node_ids(session, 4)
        # print(f"Grand child ids: {grand_child_ids}")
        # for grand_child_id in grand_child_ids:
        #     node_name = get_node_name(session, grand_child_id)
        #     print(f"Grand child node: {node_name}")
        #     # res = hapi.cookNode(session, grand_child_id, cook_options)
        #     if grand_child_id == 6:
        #         __generate_image_from_top_node(session, grand_child_id)



        # 保存
        # paramを取得
        # node_info = hapi.getNodeInfo(session, node_id)
        # node_info_param_count = node_info.parmCount
        # param_info_list = hapi.getParameters(session, node_id, 0, node_info_param_count)
        # for i in range(node_info_param_count):
        #     param_name = get_param_name(session, node_id, param_info_list[i].id)
        #     print(param_name)

        # paramを一気に設定

        # set_multi_param(session, node_id, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])


        # 保存
        # now = datetime.datetime.now()
        # output_path = "output"
        # # file名を日付+ノード名にする
        # file_name = f"{now.strftime('%Y%m%d-%H%M%S')}_{node_name}.hip"
        # hapi.saveHIPFile(session, f"{output_path}/{file_name}", True)


    except hapi.FailureError as e:
        print(f"FailureError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    close_session(session)
    print("Session cleaned up.")

    return jsonify({"message": "Node created successfully"}), 200


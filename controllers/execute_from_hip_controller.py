from flask import jsonify
import hapi

hip_path = r"/input_files/20241102-022839_ropfetch1.hip"
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, \
    close_session, get_child_node_ids

def __generate_image_from_top_node(session, top_node_id):
    # top nodeをcookPDG
    node_name = get_node_name(session, top_node_id)
    # res = hapi.cookPDG(session, top_node_id, 0, 1)

    #　cookPDGAllOutputs,ropfetchのnode_idだと「 cook_node_id should be a TOP Network」エラーが出る
    res = hapi.cookPDGAllOutputs(session, top_node_id, 0, 1)
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

        # hipファイルからnodeを作成
        res = hapi.loadHIPFile(session, hip_path, False)
        # hip_id = hapi.mergeHIPFile(session, hip_path, False)
        # count = hapi.getHIPFileNodeCount(session, hip_id)
        # node_id = hapi.getHIPFileNodeIds(session, hip_id, count)

        node_id = hapi.getNodeFromPath(session, -1, "/obj/sample_pig_image_copy1")
        node_ids = get_child_node_ids(session, node_id)
        for node_id in node_ids:
            node_name = get_node_name(session, node_id)
            if node_name == 'sample_top':
                __generate_image_from_top_node(session, node_id)
                print(f"Node name: {node_name}")





    except hapi.FailureError as e:
        print(f"FailureError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Session cleaned up.")
    close_session(session)
    return jsonify({"message": "Node created successfully"}), 200

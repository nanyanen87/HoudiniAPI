import datetime
from flask import jsonify,request,Blueprint
import sys
import hapi

from utils.hapi_utils import convert_asset_name_to_operator_name, get_param_name, set_multi_param


hip_path = r"C:\Users\hanaoka nan\AppDevelop\houdiniScript\output\20210929-161853_sample_pig_image.hip"
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, \
    close_session, convert_asset_name_to_operator_name

def get():
    # session = init_hars_session()
    # try:
    #     print("session created successfully!")
    #
    #     # hipファイルからnodeを作成
    #     hip_id = hapi.loadHIPFile(session, hip_path, False)
    #     count = hapi.getHIPFileNodeCount(session, hip_id)
    #     node_ids = hapi.getHIPFileNodeIds(session, hip_id, count)
    #     for node_id in node_ids:
    #         node_name = get_node_name(session, node_id)
    #         print(f"Loaded node: {node_name}")
    #
    #
    #
    # except hapi.FailureError as e:
    #     print(f"FailureError: {e}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #
    # hapi.cleanup(session)
    # print("Session cleaned up.")
    # # hapi.shutdown(session)
    # hapi.closeSession(session)
    return jsonify({"message": "Node created successfully"}), 200

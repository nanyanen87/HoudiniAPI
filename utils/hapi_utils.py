import datetime

import hapi
from flask import jsonify
from config import HARS_PORT, HARS_HOST, HOUDINI_PYTHON_LIB_PATH


# C言語っぽい作りになっているので、pythonっぽく使いやすいように関数を作成
# def start_hars():
#     today = datetime.date.today()
#     options = hapi.ThriftServerOptions()
#     options.timeoutMs = 10000
#     log_path = "logs/houdini-" + today.strftime("%Y%m%d") + ".log"
#     try:
#         # logファイル作成
#         open(log_path, "w").close()
#         process_id = hapi.startThriftSocketServer(options, HARS_PORT, log_path)
#     except hapi.FailureError as e:
#         print(f"FailureError: {e}")
#         return jsonify({"error": f"FailureError: {e}"}), 500
#     except Exception as e:
#         print(f"An error occurred: {e}")
"""
# library_idからlibrary_nameを取得する
"""
def get_library_name(session, library_id):
    library_id_sh = hapi.getAssetLibraryFilePath(session, library_id)
    path_name_length = hapi.getStringBufLength(session, library_id_sh)
    path_name = hapi.getString(session, library_id_sh, path_name_length)
    return path_name
"""
# library_idからasset_nameを取得する
"""
def get_asset_names(session, library_id):
    asset_count = hapi.getAvailableAssetCount(session, library_id)
    asset_name_sh_list = hapi.getAvailableAssets(session, library_id, asset_count)
    asset_names = []
    for i in range(asset_count):
        asset_name_length = hapi.getStringBufLength(session, asset_name_sh_list[i])
        asset_name = hapi.getString(session, asset_name_sh_list[i], asset_name_length)
        asset_names.append(asset_name)
    return asset_names
"""
# node_idからnode_nameを取得する
"""
def get_node_name(session, node_id):
    node_info = hapi.getNodeInfo(session, node_id)
    return __get_name_from_sh(session, node_info.nameSH)

def get_param_name(session, node_id, parm_id):
    parm_info = hapi.getParmInfo(session, node_id, parm_id)
    return __get_name_from_sh(session, parm_info.nameSH)

def set_single_param(session, node_id, param_name, value):
    param_id = hapi.getParmIdFromName(session, node_id, param_name)
    if param_id == -1:
        print(f"Parameter {param_name} not found.")
        return

    # string, int, floatで処理を分ける
    if isinstance(value, str):
        return hapi.setParmStringValue(session, node_id, param_name, 0, value)
    elif isinstance(value, int):
        return hapi.setParmIntValue(session, node_id, param_name, 0, value)
    elif isinstance(value, float):
        return hapi.setParmFloatValue(session, node_id, param_name, 0, value)
    else:
        print(f"Invalid value type: {type(value)}")
        return  False

"""
同じtypeの複数のパラメータを一気に設定する
"""
def set_multi_param(session, node_id, values):
    node_info = hapi.getNodeInfo(session, node_id)
    # string, int, floatで処理を分ける
    if isinstance(values[0], str):
        count = node_info.parmStringValueCount
        # countとvaluesの長さが違う場合はエラーを返す
        if count != len(values):
            print(f"Invalid value count: {len(values)}")
            return False

        return hapi.setParmStringValues(session, node_id, values, 0, count)
    elif isinstance(values[0], int):
        count = node_info.parmIntValueCount
        if count != len(values):
            print(f"Invalid value count: {len(values)}")
            return False

        return hapi.setParmIntValues(session, node_id, values, 0, count)
    elif isinstance(values[0], float):
        count = node_info.parmFloatValueCount
        if count != len(values):
            print(f"Invalid value count: {len(values)}")
            return False

        return hapi.setParmFloatValues(session, node_id, values, 0, count)
    else:
        print(f"Invalid value type: {type(values[0])}")
        return  False


def __get_name_from_sh(session, sh):
    str_len = hapi.getStringBufLength(session, sh)
    name = hapi.getString(session, sh, str_len)
    return name

def get_library_ids(session):
    library_count = hapi.getLoadedAssetLibraryCount(session)
    library_ids = hapi.getAssetLibraryIds(session, 0, library_count)
    return library_ids

def init_hars_session(is_in_process=False):
    session_info = hapi.SessionInfo()
    cook_options = hapi.CookOptions()

    try:
        if is_in_process:
            session = hapi.createInProcessSession(session_info)
        else:
            session = hapi.createThriftSocketSession(HARS_HOST, HARS_PORT, session_info)
            # is_valid = hapi.isSessionValid(session)
            # print(f"Session is valid: {is_valid}")
    except hapi.FailureError as e:
        print(f"FailureError: {e}")
        return jsonify({"error": f"FailureError: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500


    try:
        hapi.isInitialized(session)
        print("Session already initialized.")
    except hapi.NotInitializedError:
        hapi.initialize(session, cook_options)
        print("Session initialized.")
    return session

def close_session(session):
    hapi.cleanup(session)
    hapi.shutdown(session)
    hapi.closeSession(session)
    print(f"Session closed: {session}")

def convert_asset_name_to_operator_name(asset_name):
    array = asset_name.split("::")
    author = array[0]
    base_name = array[1].split("/")[1]
    version = array[2]

    return f"{author}::{base_name}::{version}"

def get_child_node_ids(session, node_id):
    child_count = hapi.composeChildNodeList(session, node_id,hapi.nodeType.Any,hapi.nodeFlags.Any,False)
    child_node_ids = hapi.getComposedChildNodeList(session, node_id, child_count)
    return child_node_ids
import hapi
from flask import jsonify
from config import HARS_PORT, HARS_HOST, HOUDINI_PYTHON_LIB_PATH


# C言語っぽい作りになっているので、pythonっぽく使いやすいように関数を作成

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
    str_len = hapi.getStringBufLength(session, node_info.nameSH)
    node_name = hapi.getString(session, node_info.nameSH, str_len)
    return node_name

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
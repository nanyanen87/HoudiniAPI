import datetime
from flask import jsonify
import hapi
from config import HARS_PORT, HARS_HOST
from utils.hapi_utils import get_library_name, get_asset_names, get_node_name, get_library_ids, init_hars_session, close_session


def execute():
    session = init_hars_session()

    try:
        # node_id = hapi.createNode(session, -1, 'Sop/curve')
        # node_info = hapi.getNodeInfo(session, node_id)
        # str_len = hapi.getStringBufLength(session, node_info.nameSH)
        # node_name = hapi.getString(session, node_info.nameSH, str_len)
        # print(f"Created node: {node_name}")
        # today = datetime.date.today()
        #
        # output_path = "output"
        # # file名を日付+ノード名にする
        # file_name = f"{today.strftime('%Y%m%d')}_{node_name}.hip"
        # hapi.saveHIPFile(session, f"{output_path}/{file_name}", True)

        print("Session created successfully!" + str(session))
        # 読み込まれているlibraryを取得
        library_count = hapi.getLoadedAssetLibraryCount(session)
        library_ids = hapi.getAssetLibraryIds(session, 0, library_count)
        # library_ids = get_library_ids(session)
        # for library_id in library_ids:
        #     library_name = get_library_name(session, library_id)
        #     print(f"Loaded asset library id:{library_id} " + f"library name: {library_name}")

        # assets = get_asset_names(session, 5)
        # print(f"Available assets: {assets}")




    except hapi.FailureError as e:
        print(f"FailureError: {e}")
        close_session(session)
        return jsonify({"error": f"FailureError: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        close_session(session)
        return jsonify({"error": f"An error occurred: {e}"}), 500

    close_session(session)
    return jsonify({"message": "Node created successfully"}), 200
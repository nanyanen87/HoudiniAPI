import pkgutil
import importlib
from flask import Blueprint, Flask

"""
controllersディレクトリ内の全てのコントローラーを登録する
"""
def register_controllers(app: Flask):
    # controllersディレクトリの全てのファイルを取得 再帰的はこの方法じゃ無理
    print("Registering controllers...")
    for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f'{__name__}.{module_name}')
        # ファイルパスから_controllerを取り除いてend_pointを取得
        end_point = module_name.replace('_controller', '')

        bp = Blueprint(end_point, __name__, url_prefix=f'/api/{end_point}')
        # 各モジュールのメソッドを登録
        if hasattr(module, 'get'):
            bp.add_url_rule('', view_func=module.get, methods=['GET'])
        if hasattr(module, 'post'):
            bp.add_url_rule('', view_func=module.post, methods=['POST'])
        if hasattr(module, 'put'):
            bp.add_url_rule('', view_func=module.put, methods=['PUT'])
        if hasattr(module, 'delete'):
            bp.add_url_rule('', view_func=module.delete, methods=['DELETE'])

        app.register_blueprint(bp)
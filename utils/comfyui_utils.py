import json
from urllib import request, parse
import dotenv
import uuid
import os

dotenv.load_dotenv()
host = os.getenv("HOST")
port = int(os.getenv("PORT"))
client_id = str(uuid.uuid4())
comfy_ui_domain = os.getenv("COMFY_UI_DOMAIN")

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}

"""
# comfyuiのapiを使うためのクラス
"""

def __queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }

    req =  request.Request("https://{}/prompt".format(comfy_ui_domain), data=data, headers=headers)
    return json.loads(request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = parse.urlencode(data)
    with request.urlopen("https://{}/view?{}".format(comfy_ui_domain, url_values)) as response:
        return response.read()

def get_images(ws, prompt):
    prompt_id = __queue_prompt(prompt)['prompt_id']
    output_images = {}
    current_node = ""
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['prompt_id'] == prompt_id:
                    if data['node'] is None:
                        break #Execution is done
                    else:
                        current_node = data['node']
        else: # 処理結果の画像データ
            if current_node == 'save_image_websocket_node':
                images_output = output_images.get(current_node, [])
                images_output.append(out[8:])
                output_images[current_node] = images_output

    return output_images

import requests
from utils import load_config
from io import BytesIO
from PIL import Image
import os

def resize_image_if_needed(image_data, max_size=3 * 1024 * 1024):
    """
    画像が指定されたサイズを超える場合は、画像のサイズを縮小する。

    Args:
        image_data (bytes): 画像データ。
        max_size (int): 最大ファイルサイズ（バイト）。

    Returns:
        bytes: サイズ変更後の画像データ。
    """
    if len(image_data) > max_size:
        image = Image.open(BytesIO(image_data))
        new_size = (image.width // 2, image.height // 2)
        image = image.resize(new_size, Image.LANCZOS)

        output = BytesIO()
        image_format = image.format if image.format else 'JPEG'
        image.save(output, format=image_format)
        return output.getvalue()
    return image_data

def send_line_notify(message, image_paths=None, config_path='config.json'):
    """
    LINE Notifyを使用してメッセージとオプションで画像を送信する関数。
    複数の画像パスをリストとして受け取ることができます。

    Args:
        message (str): 送信するメッセージ。
        image_paths (list): 送信する画像のパスのリスト。
        config_path (str): 設定ファイルのパス。

    Returns:
        None
    """
    # 設定ファイルを読み込む
    config = load_config(config_path)

    # 設定ファイルからトークンを取得
    token = config['token']

    url = 'https://notify-api.line.me/api/notify'

    headers = {'Authorization': f"Bearer {token}"}
    params = {'message': message}

    # 画像がリストとして渡されている場合に対応
    if image_paths is not None:
        if not isinstance(image_paths, list):
            image_paths = [image_paths]

        for image_path in image_paths:
            if image_path is not None:
                with open(image_path, 'rb') as img_file:
                    img_data = img_file.read()
                    img_data = resize_image_if_needed(img_data)
                    files = {'imageFile': BytesIO(img_data)}
                    files['imageFile'].name = os.path.basename(image_path)

                    # LINE Notify APIにリクエストを送信
                    res = requests.post(url, headers=headers, params=params, files=files)

                    # レスポンスを出力
                    print(f"Sent {image_path}: {res.status_code} {res.text}")
    else:
        # 画像がない場合はメッセージのみ送信
        res = requests.post(url, headers=headers, params=params)
        print(f"Sent message: {res.status_code} {res.text}")

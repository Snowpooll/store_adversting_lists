import os
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_latest_directory(base_path):
    # 指定されたディレクトリ内の全てのサブディレクトリを取得
    subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    # サブディレクトリ名が 'predict' で始まり、その後に数字が続くものをフィルタリング
    predict_dirs = [d for d in subdirs if d.startswith('predict') and d[7:].isdigit()]

    if not predict_dirs:
        raise ValueError("No valid 'predict' directories found")

    # サブディレクトリ名を数値に変換し、ソートして最新のディレクトリを特定
    latest_dir = max(predict_dirs, key=lambda x: int(x[7:]))

    return os.path.join(base_path, latest_dir)

def get_image_files(directory):
    # 指定されたディレクトリ内の全ての画像ファイルのパスを取得
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    image_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(image_extensions)]
    return image_files


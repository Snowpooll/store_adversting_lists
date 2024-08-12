# image_downloader.py

import os
import json
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def load_config(config_file):
    """設定ファイルからコンフィグを読み込む"""
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def open_link_in_safari(url):
    """指定されたURLをSafariで開く"""
    service = SafariService()
    driver = webdriver.Safari(service=service)
    driver.get(url)
    time.sleep(3)  # リンクを開いた後に3秒間待機
    return driver

def get_images_from_container(driver, base_xpath):
    """指定されたXPathから画像URLを取得する"""
    image_urls = []
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, base_xpath))
        )
        images = container.find_elements(By.TAG_NAME, 'img')
        
        for img in images:
            src = img.get_attribute('src')
            print(f'Checking image source: {src}')  # ログ追加
            if 'index/img' in src:
                image_urls.append(src)
                print(f'Found image: {src}')
    except Exception as e:
        print(f'Error finding images: {e}')
    return image_urls

def download_images(image_urls):
    """画像URLから画像をダウンロードする"""
    images = []
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            images.append(image)
            print(f'Downloaded image_{i}.jpg')
        else:
            print(f'Failed to download {url}')
    return images

def merge_images(images, output_path):
    """複数の画像を結合して保存する"""
    if not images:
        print("No images to merge.")
        return

    widths, heights = zip(*(img.size for img in images))
    total_height = sum(heights)
    max_width = max(widths)

    combined_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    combined_image.save(output_path)
    print(f'Saved combined image as {output_path}')

def download_and_merge_images(config_file, url):
    """画像をダウンロードして結合するメイン関数"""
    config = load_config(config_file)
    driver = open_link_in_safari(url)

    base_xpath_images = config['base_xpath_images']
    image_urls = get_images_from_container(driver, base_xpath_images)
    driver.quit()
    
    if image_urls:
        images = download_images(image_urls)
        if images:
            current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = 'images'
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'combined_image_{current_timestamp}.jpg')
            merge_images(images, output_path)
            return output_path  # 生成されたファイル名を返す
    return None  # 画像がなかった場合はNoneを返す

# example_usage.py

from gmail_url_extractor import get_first_unread_email_url
from image_downloader import download_and_merge_images
from google.cloud import vision
from line_notify import send_line_notify
import io
import json

def load_settings(file_path='settings.json'):
    with open(file_path, 'r', encoding='utf_8') as settings_json:
        return json.load(settings_json)

def detect_text(image_path):
    """OCRで画像からテキストを抽出"""
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    full_text_annotation = response.full_text_annotation

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # # OCRの結果をデバッグ表示
    # full_text_annotation = response.full_text_annotation
    # print("Extracted Text:", full_text_annotation.text)

    return full_text_annotation.text

def search_words(text, keywords):
    """抽出したテキストからキーワードを検索"""
    hitwords = []
    for keyword in keywords:
        if keyword in text:
            hitwords.append(keyword)
    return hitwords

def main():
    # 設定を読み込む
    settings = load_settings()
    
    # GmailからURLを取得
    url = get_first_unread_email_url('【Shufoo!】お気に入り店舗新着チラシお知らせメール')  # '特売情報'はメールの件名に含まれるキーワード
    
    if url:
        print(f"Processing URL: {url}")
        # 画像をダウンロードしてOCRを実行
        output_path = download_and_merge_images('config.json', url)
        
        if output_path:
            extracted_text = detect_text(output_path)
            hitwords = search_words(extracted_text, settings["keywords"])
            
            if hitwords:
                message = "特売リスト: " + ", ".join(hitwords)
                send_line_notify(message, output_path)
            else:
                print("マッチしたキーワードはありませんでした。")
    else:
        print("未読メールが見つかりませんでした。")

if __name__ == '__main__':
    main()

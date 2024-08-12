# store_adversting_lists
OCR the content of the flyer If your purchase matches Send product name and flyer image with line notify

gmailで件名を指定し、未読の最新のメールを取得後にURLを抽出、  
抽出したURLを元にブラウザを開き画像をダウンロード  
ダウンロード画像へcloud vision api を実行し  
購入リストにマッチしたものを
LINE norifyで買い物リストが送信されます  


## 動作環境
M1 MacbookAir 16GB で動作しています、  
対象となるチラシは shufoo というサイトです  
お気に入り店舗を登録する必要があります

使用にあたり
pip install -r requirements.txt  
を実行後  
image_ocr_notifier.py  
を実行します

キーワードリストと商品名を関連づけるため  
settings.json
で設定をしています。
商品名を追加したい場合は対応する商品名を追記してください  

LINE Notifyを使うため  
config.json  
へ取得したトークンを記述してください  

サイトの構成が変わるため、この場合  
config.json  
でxpathの設定を変更する必要があります

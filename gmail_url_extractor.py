import os.path
import base64
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 認証情報ファイルのパス
CREDENTIALS_FILE = 'path/to/credentials.json'
TOKEN_FILE = 'token.json'

# Gmail APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Gmail APIに認証し、サービスを構築します。"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def extract_first_url(text):
    """テキストから最初のURLを抽出します。"""
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

def get_message_body(payload):
    """メールの本文を取得します。"""
    body = ""
    
    if 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    elif 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                body_data = part['body'].get('data')
                if body_data:
                    body += base64.urlsafe_b64decode(body_data).decode('utf-8')
    
    return body

def get_first_unread_email_url(subject_query):
    """指定された件名を持つ未読メールから最初のURLを取得します。"""
    service = authenticate_gmail()

    query = f'is:unread subject:"{subject_query}"'
    results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
        return None
    
    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    msg_payload = msg['payload']
    
    msg_body = get_message_body(msg_payload)
    first_url = extract_first_url(msg_body)
    
    return first_url

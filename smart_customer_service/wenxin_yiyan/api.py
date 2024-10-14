# wenxin_yiyan/api.py
import requests
import json

APP_ID = 'app-0PmXo6CT'  # 替换为你的实际APPID
API_KEY = 'YOUR_API_KEY'  # 替换为你的实际API_KEY
SECRET_KEY = 'YOUR_SECRET_KEY'  # 替换为你的实际SECRET_KEY


def get_wenxin_response(question):
    url = 'https://api.wenxin.baidu.com/aip/v3/ai_chat'
    headers = {
        'content-type': 'application/json'
    }
    params = {
        'access_token': get_access_token()
    }
    data = {
        "text": question,
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))
    result = response.json()
    if result['code'] == 200:
        return result['data']['response']
    else:
        return "抱歉，我无法理解您的问题。"


def get_access_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': APP_ID,
        'client_secret': SECRET_KEY,
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result['access_token']
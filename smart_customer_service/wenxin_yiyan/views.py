import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

ERNIE_BOT_APP_ID = '115781939'
ERNIE_BOT_API_KEY = 'xKR8ziUuw9GE3MMf6h9oWvGb'
ERNIE_BOT_SECRET_KEY = '4dAhKD57gZgYFIwUl5EmeAaW6tfTq4F7'


def chatbot_home(request):
    return render(request, 'chat_window.html')


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": ERNIE_BOT_API_KEY, "client_secret": ERNIE_BOT_SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


@csrf_exempt
def chatbot_response(request):
    # 解析请求体中的 JSON 数据
    try:
        data = json.loads(request.body)
        query = data.get('message', '')  # 取出 message 对应的值
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    # 文心一言 API URL 和 Token
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        # 解析响应 JSON 数据
        response_data = response.json()
        # 提取结果
        result = response_data.get('result', '抱歉，我没有找到合适的回答。')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to parse response JSON'}, status=500)

    return JsonResponse({'response': result})

import requests
import json

# 自己造轮，丰衣足食 给封装SDK的自己点赞！

def SendGroupMsg(access_token,msgParam,msgKey,openConversationId,robotCode):
    baseUrl = "https://api.dingtalk.com"
    url = "/v1.0/robot/groupMessages/send"
    headers = {
        "Content-Type": "application/json",
        "x-acs-dingtalk-access-token": access_token
    }
    data = {
        "msgKey": msgKey,
        "msgParam": msgParam,
        "msgtype": msgKey,
        "openConversationId": openConversationId,
        "robotCode": robotCode,
    }
    response = requests.post(url=baseUrl+url, headers=headers, data=json.dumps(data, ensure_ascii=False, indent=4))
    return response.json()

def getAccessToken(appKey, appSecret):
    # 生成的AccessToken时效性较短，请生成后立即使用，此接口有次数调用限制
    baseUrl = "https://api.dingtalk.com"
    url = "/v1.0/oauth2/accessToken"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "appKey": appKey,
        "appSecret": appSecret
    }
    response = requests.post(url=baseUrl+url, headers=headers, data=json.dumps(data, ensure_ascii=False, indent=4))
    jsonData = response.json()
    return jsonData["accessToken"]
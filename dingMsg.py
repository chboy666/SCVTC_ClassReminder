from DingTalkSDK import main as Ding #引入钉钉SDK
import json

# =====================【必填】===============================
# 需要在这里配置钉钉发信参数，发信参数需要查看钉钉开放平台获取
# 钉钉机器人的创建方法这里忽略，钉钉开放平台：https://open.dingtalk.com 自行查阅
ding_sdk_config_appKey = ""
ding_sdk_config_appSecret = ""
ding_sdk_config_openConversationId = ""
ding_sdk_config_robotCode = ""
# =====================【必填】===============================

def Ding_SendGroupMsg(msg_title,msg_text):
    parms_accesstToken = Ding.getAccessToken(ding_sdk_config_appKey,ding_sdk_config_appSecret)
    parms_msgKey = "sampleMarkdown"
    parms_msgParam = {
        "title": msg_title,
        "text": msg_text
    }
    parms_msgParam = json.dumps(parms_msgParam, ensure_ascii=False)
    parms_openConversationId = ding_sdk_config_openConversationId
    parms_robotCode = ding_sdk_config_robotCode

    msg = Ding.SendGroupMsg(parms_accesstToken,
                            parms_msgParam,
                            parms_msgKey,
                            parms_openConversationId,
                            parms_robotCode)

    print(f"√ 钉钉消息发送成功:{msg}")
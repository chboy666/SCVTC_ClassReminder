import requests
import json
import base64
import time
import config
import utils

def api_login_pc(): #返回 cookie 数据
    '''
    使用 pc 协议 api，获取 cookie 信息。需自行解析返回信息。
    '''
    if not api_login_checkparm():
        return False
    http_url = config.web_system_url + 'api/api/login?'
    http_parm = {
        "userName":config.web_system_login_username,
        "token":base64.b64encode(config.web_system_login_password.encode()).decode(),
        "pattern":"manager-login",
        "timestamp":int(time.time() * 1000),
        "_t":int(time.time())
    }
    http_header = {
        "content-type":"application/x-www-form-urlencoded;charset=utf-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "referer":config.web_system_url
    }
    http_response = requests.post(http_url,data=http_parm,headers=http_header)
    # 遍历cookies
    cookies_dict= {}
    for cookie in http_response.cookies:
        cookies_dict[cookie.name] = cookie.value
    print(f"√ 账号登录成功，已获取账户CK:{cookies_dict}")
    return True,cookies_dict
def api_login_checkparm():
    if config.web_system_url == "" or config.web_system_login_username == "" or config.web_system_login_password == "":
        return False
    else:
        return True
def api_User_Info(cookie):
    '''
    使用 pc 协议 api，通过获取用户信息以查看cookie是否正确。
    '''
    http_url = config.web_system_url + '/jwgr/api/student/studentInfo/querySelf?'+ "_t=" + str(int(time.time()))
    http_data = "{}"
    http_header = {
        "content-type":"application/json;charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "referer":config.web_system_url,
    }
    http_response = requests.post(http_url,headers=http_header,data=http_data,cookies = cookie)
    response = json.loads(http_response.text)
    if response['code'] == 200:
        print(f"√ CK登录成功，当前登录账号[{response['data']['rows'][0]['xm']}],学号[{response['data']['rows'][0]['xh']}]")
        return True,response['data']['rows'][0]['xh']
    else:
        print(f"× CK登录失败：{http_response.text}")
        return False

def api_Semester_Info(cookie):
    '''
    获取当前学期数据
    :param cookie: 用于访问的ck
    :return: 返回学期数据
    '''
    http_url = config.web_system_url + 'jwgr/api/baseInfo/semester/selectCurrentXnXq?' + "_t=" + str(int(time.time()))
    http_header = {
        "content-type":"application/json;charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "referer":config.web_system_url,
    }
    http_response = requests.get(http_url,headers=http_header,cookies = cookie)
    response = json.loads(http_response.text)
    if response['code'] == 200:
        return response['data']
    else:
        return False

def api_Course_ScheduleQuery(cookie,semester,studentId):
    '''
    获取课表数据
    :param cookie: 用于访问的ck
    :param semester: 学期
    :param weekday: 第几周
    :param studentId: 学号
    :return: 返回课表数据
    '''
    http_url = config.web_system_url + 'jwgr/api/arrange/CourseScheduleAllQuery/studentCourseSchedule?' + "_t=" + str(int(time.time()))
    http_data = {
            "semester": semester,
            "weeks": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            "querySource": "single",
            "oddOrDouble": 1,
            "startWeek": 1,
            "stopWeek": 20,
            "studentId": studentId
}
    http_header = {
        "content-type":"application/json;charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "referer":config.web_system_url,
    }
    http_response = requests.post(http_url,headers=http_header,data=json.dumps(http_data),cookies = cookie)
    response = json.loads(http_response.text)
    if response['code'] == 200:
        print("√ 获取课表数据成功,正在解析中...")
        return True,response['data']
    else:
        print(f"× 获取课表数据失败：{http_response.text}")
        return False
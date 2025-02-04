'''
定时任务，请配置crontab: * * * * *
用于课表通知。
'''
import utils
import configparser
from datetime import datetime, time, timedelta
import dingMsg


def cronNotice():
        # 先前操作
        sendMsgText_header = ""
        sendMsgText_footer = ""
        # 获取配置文件
        config = configparser.ConfigParser()
        config.read('data.ini',encoding='utf-8')
        # 获取当前时间
        current_date = datetime.now().time()
        # 获取课表
        CourseData = config.sections()
        for i,CourseData_item in enumerate(CourseData):
            # 分割文本，获取相应的内容
            CourseData_item_list = CourseData_item.split("_")
            CourseData_item_weekday = CourseData_item_list[0] # 这个参数一般不用管，这个参数没什么用
            CourseData_item_time = CourseData_item_list[1]
            CourseData_item_j = CourseData_item_list[2]

            # 查看通知时间
            CourseData_item_notice_time_obj = get_CourseRules(int(CourseData_item_time))
            # 将本地时间和通知时间转换为dt对象，方便后续计算时间间隔
            current_date_dt = datetime.combine(datetime.today(), current_date)
            CourseData_item_notice_time_dt = datetime.combine(datetime.today(), CourseData_item_notice_time_obj)
            # 计算直接差值
            CourseData_item_notice_time_direct = abs((CourseData_item_notice_time_dt - current_date_dt).total_seconds())
            # 处理跨越午夜的情况
            if current_date_dt < CourseData_item_notice_time_dt:
                diff_with_next_day = (CourseData_item_notice_time_dt - current_date_dt + timedelta(days=1)).total_seconds() % (24 * 3600)
            else:
                diff_with_next_day = (current_date_dt - CourseData_item_notice_time_dt + timedelta(days=1)).total_seconds() % (24 * 3600)
            # 取两者中的最小值作为实际差值
            CourseData_item_notice_time_direct = min(CourseData_item_notice_time_direct, diff_with_next_day)
            # 判断时间差是否在2分钟(120秒)内
            if CourseData_item_notice_time_direct <= 120:
                # 判断当前是否重复通知
                if config[CourseData_item]["status"] == "1":
                    print(f"× 本轮课程已通知过，本轮课程[{CourseData_item}]已通知，本次跳过该课程的通知服务")
                    continue
                # 处理发送通知相关逻辑，编辑发帖模版：
                # 获取相对应的参数
                CourseData_item_CourseName = config.get(CourseData_item, "CourseName")
                CourseData_item_CourseCode = config.get(CourseData_item, "CourseCode")
                CourseData_item_TeacherName = config.get(CourseData_item, "TeacherName")
                CourseData_item_TeacherCode = config.get(CourseData_item, "TeacherCode")
                CourseData_item_Weeks = config.get(CourseData_item, "Weeks")
                CourseData_item_ClassroomName = config.get(CourseData_item, "ClassroomName")
                CourseData_item_ClassroomCode = config.get(CourseData_item, "ClassroomCode")
                CourseData_item_NumberOfStudent = config.get(CourseData_item, "NumberOfStudent")
                CourseData_item_TeachingClassName = config.get(CourseData_item, "TeachingClassName")

                CourseData_item_classBeginTimedt = datetime.combine(datetime.today(), get_CourseTimes(int(CourseData_item_time))) # 获取正式上课时间
                # 更新状态，防止多次通知
                config[CourseData_item]["status"] = "1"
                with open('data.ini', 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
                sendMsgText_title =  f"上课通知:{CourseData_item_CourseName}({CourseData_item_classBeginTimedt})"
                sendMsgText_header = f"""
#### 今日本轮课程上课提醒：
> 推送时刻：{CourseData_item_notice_time_dt}

> 本次开课课程：**{CourseData_item_CourseName}**

> 上课时段：星期{utils.parse_str.int_to_chinese(int(CourseData_item_weekday))} 第{CourseData_item_time}节 第{CourseData_item_j}轮通知
#### 本轮课程详情：

- **课程名称**: {CourseData_item_CourseName}({CourseData_item_CourseCode})
- **教师姓名**: {CourseData_item_TeacherName}({CourseData_item_TeacherCode})
- **时间**: {CourseData_item_classBeginTimedt}(即将开始)
- **地点**: {CourseData_item_ClassroomName}({CourseData_item_ClassroomCode})
- **周数**: {CourseData_item_Weeks}(本次课相同时间下)
- **上课人数**: {CourseData_item_NumberOfStudent}人
- **上课班级**: {CourseData_item_TeachingClassName}

"""
                k = 0
                l = 0
                # 获取后续课程数据
                for j, CourseData_item in enumerate(CourseData):
                    if i > j:
                        l += 1 #自增计数器
                        if l == 1:
                            sendMsgText_header += """
---
#### 今日已上课程：                            
"""
                        CourseData_item_list = CourseData_item.split("_")
                        CourseData_item_time = CourseData_item_list[1]
                        CourseData_item_classBeginTimedt = datetime.combine(datetime.today(), get_CourseTimes(int(CourseData_item_time)))  # 获取正式上课
                        CourseData_item_CourseName = config.get(CourseData_item, "CourseName")
                        CourseData_item_TeacherName = config.get(CourseData_item, "TeacherName")
                        sendMsgText_header +=f'''
                        
{l}:{CourseData_item_CourseName}({CourseData_item_TeacherName}) - {CourseData_item_classBeginTimedt}

'''
                    if i == j:
                        continue
                    if i < j:
                        k += 1 #自增计数器
                        if k == 1:
                            sendMsgText_header += """
---
#### 今日剩余课程：
                                                  """
                        # 获取相对应的参数
                        CourseData_item_list = CourseData_item.split("_")
                        CourseData_item_weekday = CourseData_item_list[0]  # 这个参数一般不用管，这个参数没什么用
                        CourseData_item_time = CourseData_item_list[1]
                        CourseData_item_j = CourseData_item_list[2]
                        CourseData_item_CourseName = config.get(CourseData_item, "CourseName")
                        CourseData_item_CourseCode = config.get(CourseData_item, "CourseCode")
                        CourseData_item_TeacherName = config.get(CourseData_item, "TeacherName")
                        CourseData_item_TeacherCode = config.get(CourseData_item, "TeacherCode")
                        CourseData_item_Weeks = config.get(CourseData_item, "Weeks")
                        CourseData_item_ClassroomName = config.get(CourseData_item, "ClassroomName")
                        CourseData_item_ClassroomCode = config.get(CourseData_item, "ClassroomCode")
                        CourseData_item_NumberOfStudent = config.get(CourseData_item, "NumberOfStudent")
                        CourseData_item_TeachingClassName = config.get(CourseData_item, "TeachingClassName")

                        CourseData_item_classBeginTimedt = datetime.combine(datetime.today(), get_CourseTimes(int(CourseData_item_time)))  # 获取正式上课时间

                        sendMsgText_footer += f"""
***[{int(k)}]***
- **课程名称**: {CourseData_item_CourseName}({CourseData_item_CourseCode})
- **教师姓名**: {CourseData_item_TeacherName}({CourseData_item_TeacherCode})
- **时间**: {CourseData_item_classBeginTimedt}
- **地点**: {CourseData_item_ClassroomName}({CourseData_item_ClassroomCode})
- **周数**: {CourseData_item_Weeks}(相同课相同时间下)
- **上课人数**: {CourseData_item_NumberOfStudent}人
- **上课班级**: {CourseData_item_TeachingClassName}
                                            """
                sendMsgText_footer+='''
---
> 如果对课程有任何疑问，请及时联系教务处;

> 祝大家学习愉快！ By Chboy
                    '''
                dingMsg.Ding_SendGroupMsg(msg_title=f"{sendMsgText_title}", msg_text=sendMsgText_header+sendMsgText_footer)
                # 输出
                print(f"√ {sendMsgText_title}即将开始,通知已发送,发送时间:[{current_date_dt}]")


def get_CourseTimes(time):
    '''
    课程时间(上课时间)
    :param time:
    :return:
    '''
    Times = ""
    if time == 1:
        Times = "8:50"
    elif time == 2:
        Times = "10:30"
    elif time == 3:
        Times = "14:00"
    elif time == 4:
        Times = "15:40"
    elif time == 5:
        Times = "19:40"
    if Times == "":
        exit()
    return datetime.strptime(Times, '%H:%M').time()

def get_CourseRules(time):
    '''
    通知时间(消息提醒时间)
    :param time:
    :return:
    '''
    rulesTime = ""
    if time == 1:
        rulesTime = "8:20"
    elif time == 2:
        rulesTime = "10:00"
    elif time == 3:
        rulesTime = "13:35"
    elif time == 4:
        rulesTime = "15:10"
    elif time == 5:
        rulesTime = "19:25"
    if rulesTime == "":
        print(f"× 规则时刻表无法获取相应规则:{time},请检查设置")
        exit()
    else:
        print(f"√ 课表运行时间[{rulesTime}]在课表时间内,已命中规则")
    rulesTime_obj = datetime.strptime(rulesTime, '%H:%M').time()
    return rulesTime_obj

cronNotice()
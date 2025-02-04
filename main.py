'''
读取教务系统中的课表，并写入本地文件，后期定时任务直接读取本地文件中的内容
'''
import json
import os
from datetime import datetime
import configparser
from ScheduleApi import main as Api
import utils

# 获取ck
Api_Cookie = Api.api_login_pc()[1]

# 判断ck是否正确，如果不正确则退出
Api_LoginFlag = Api.api_User_Info(Api_Cookie)
if not Api_LoginFlag[0]:
    exit()
Api_UserId = Api_LoginFlag[1]

# 获取学期信息，判断当前学期、周数
Semester_data = Api.api_Semester_Info(Api_Cookie)

# ===========================
# 学期时间解析处理块

Semester_data_code = Semester_data['semester'] #学期代码
Semester_data_ksrq = datetime.strptime(Semester_data['ksrq'], "%Y-%m-%d") #开学日期，用此参数计算当前周
Semester_data_jsrq = datetime.strptime(Semester_data['jsrq'], "%Y-%m-%d") #结束日期，用此参数计算当前周

# 获取当前日期
current_date = datetime.now()
# 检查当前日期是否在学期范围内
if Semester_data_ksrq <= current_date <= Semester_data_jsrq:
    # 计算这是学期中的第几周
    Semester_today_weekday = (current_date - Semester_data_ksrq).days // 7 + 1
    # 计算今天是星期几(0=星期一，6=星期日)
    Semester_today_day = current_date.weekday() + 1
    print(f"√ 当前日期[{current_date}]在本学期内，本学期第{Semester_today_weekday}周，今天是星期{Semester_today_day}, 开始获取课表...")
else:
    print(f"× 当前日期[{current_date}]不在本学期内，跳过执行。")
    exit()
# ===========================
Api_CourseFlag = Api.api_Course_ScheduleQuery(Api_Cookie, Semester_data_code, Api_UserId)

if not Api_CourseFlag[0]:
    print(f"× 获取课表失败，请检查教务系统是否正常。")
    exit()

Api_CourseData = Api_CourseFlag[1]

# 创建配置项对象
config = configparser.ConfigParser()
# ===========================
# 课程表处理块
for i,CourseData_item in enumerate(Api_CourseData):
    # 周数计算
    CourseData_item_week_Name = CourseData_item["week"]["weekName"] # 星期一
    CourseData_item_week_Code = int(CourseData_item["week"]["weekCode"]) # 1
    if CourseData_item_week_Code == 1: #每周第一天为星期天，在此需转换为中国计算方法
        CourseData_item_week_Code = 7
    else:
        CourseData_item_week_Code = CourseData_item_week_Code - 1
    # 上课时间计算
    CourseData_item_time_Name = CourseData_item["time"]["timeName"] # 第1-2节
    CourseData_item_time_Code = CourseData_item["time"]["sort"] # 1

    for j,CourseData_item_courseList in enumerate(CourseData_item["courseList"]):
        # 当前前提下的课程List
        CourseData_item_courseList_CourseName = CourseData_item_courseList["courseName"] # Linux操作系统
        CourseData_item_courseList_CourseCode = CourseData_item_courseList["courseCode"] # 021xxxxx
        CourseData_item_courseList_TeacherName = CourseData_item_courseList["teacherName"] # 李x
        CourseData_item_courseList_teacherCode =  CourseData_item_courseList["teacherCode"] # 2023xxxxx
        CourseData_item_courseList_weeks = CourseData_item_courseList["weeks"] # 7-8 此门课此时间的起始周和结束周
        CourseData_item_courseList_classroomName = CourseData_item_courseList["classroomName"] # B5-101机房
        CourseData_item_courseList_classroomCode = CourseData_item_courseList["classroomCode"] # B5-101
        CourseData_item_courseList_numberOfStudent = CourseData_item_courseList["numberOfStudent"] # 100 上课人数
        CourseData_item_courseList_teachingClassName = CourseData_item_courseList["teachingClassName"] # 上课的班级名称
        # 判断是否是当前系统相对应的时间，若不是，则跳过
        if utils.parse_str.is_within_week_range(str(Semester_today_weekday), CourseData_item_courseList_weeks) and CourseData_item_week_Code == Semester_today_day:
            # 写入的配置项规则：星期几_上课节数_j计次数(防止重复)
            config[str(CourseData_item_week_Code) + "_" + str(CourseData_item_time_Code) + "_" + str(j)] = {
                "CourseName": CourseData_item_courseList_CourseName,
                "CourseCode": CourseData_item_courseList_CourseCode,
                "TeacherName": CourseData_item_courseList_TeacherName,
                "TeacherCode": CourseData_item_courseList_teacherCode,
                "Weeks": CourseData_item_courseList_weeks,
                "ClassroomName": CourseData_item_courseList_classroomName,
                "ClassroomCode": CourseData_item_courseList_classroomCode,
                "NumberOfStudent": CourseData_item_courseList_numberOfStudent,
                "TeachingClassName": CourseData_item_courseList_teachingClassName,
                "status": 0
            }
# ===========================
with open('data.ini', 'w', encoding='utf-8') as configfile:
    config.write(configfile)
    print(f"√ 课表写入成功,程序即将退出")
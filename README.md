[![GitHub stats](https://github-readme-stats.vercel.app/api?username=chboy666&show_icons=true&theme=dark)](https://github.com/chboy666)

# SCVTC_教务系统课程提醒自动化程序

## 项目简介

本项目基于`python`自动化程序实现SCVTC_教务系统的课程提醒功能，帮助学生及时了解课程安排，避免错过重要的课程信息。
该程序通过抓取教务系统的课程表数据并进行处理，在设置的规定时间自动发送课程提醒通知。

**此项目配合[青龙面板](https://github.com/whyour/qinglong)一起使用更搭哦~**

## 功能特点

- 自动从SCVTC学院的教务系统中抓取课程表数据。
- 根据设定的提醒时间，自动从钉钉发送课程提醒通知。
- 支持自定义提醒时间和上课时间。
- 简单易用，已经将需要自己设置的参数内容提取了出来，傻瓜式配置即可。

## 技术栈

- Python(100%)

## 劝退警告

- 本脚本使用Python获取课程表信息，并且在上课前30分钟通过钉钉发信提醒用户。故需要配置钉钉发信参数，如果不愿意配置，则此项目可能不适合你。
- 如果你不想折腾，可能这个项目也不适合你，但你若有问题欢迎提出issue，我也会尽力帮助你，但请遵循[《**提问的智慧** - **How To Ask Questions The Smart Way**》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)。
- 如果你也是SCVTC(川教)的学生，那么你可以完全不用改任何的代码，直接部署之后填入相应的配置参数，即可使用。

## 安装与使用

### 创建钉钉机器人

首先，需要在[钉钉OA平台](https://oa.dingtalk.com)创建企业/组织，再到[钉钉开发平台](https://open.dingtalk.com)选择刚才创建的企业/组织，之后创建应用并创建机器人。

在钉钉开放平台获取下述相应参数，并把相应参数填入`/dingMsg.py`中。

```python
ding_sdk_config_appKey = ""
ding_sdk_config_appSecret = ""
ding_sdk_config_openConversationId = ""
ding_sdk_config_robotCode = ""
```

### 配置教务系统参数

- 配置教务系统的登录网址、登录名、密码，以获取课程表信息。

- Ps:教务系统默认封了国外IP，如果需要将自动化程序部署在国外服务器，需自行在国内服务器中部署反向代理，否则教务系统无法连接！

- 把相应参数填入`/config.py`中。

```python
web_system_url = 'https://jwxt.scvtc.edu.cn/' # 教务系统中的 url 链接
web_system_login_username = '' # 教务系统欲登录的 用户名
web_system_login_password = '' # 教务系统欲登录中的 密码
```

### 环境要求

- Python 3.1及以上版本
- 相关Python库：`requests`, `json`, `datetime`

### 部署步骤(二选一)

#### 克隆项目到本地：

```bash
git clone https://github.com/chboy666/SCVTC_ClassReminder.git
```

#### 在Releases中下载成品代码：

- 截止撰稿前，最近一次更新版本是`250204`，若发现有最新版请自行更改下述链接。

https://github.com/chboy666/SCVTC_ClassReminder/releases/tag/250204

### 程序构造

- 程序提供了两个`python`文件，分别为`/main.py`、`/cron.py`。

1. `Main.py`：主函数，负责当天课程表的数据爬取，并把爬取的数据写入到项目主路径下。
2. `cron.py`：Cron（定时任务）函数，负责消息推送。读入主函数爬取的数据，并检测当前的运行时间是否在上课前30分钟的阈值内，如果在，则推送消息。

- 一般主函数在每天的凌晨执行一次（具体时间可自定义，尽量在每天上课之前执行），以获取当天课程表的数据。Crontab我设置的是`0 3 * * *`
- 一般Cron（定时任务）函数每分钟执行一次，Crontab请设置（务必设置）`* * * * *`
- 若搭配青龙面板，请也遵循上述规则添加上述两个自动化任务。
- 本项目会在系统中写入、修改文件，故请确保本项目在系统中权限为：`755`

### 异常容错机制

- 程序内已做好异常容错机制，程序会尝试在发信推送前的2分钟进行第一次发信，如果第一次发信成功，则直接跳过第二次发信。
- 如果第一次发信失败，则会在发信推送前的1分钟进行第二次发信。

---

- 在每次发信成功后，程序会自动锁定当前课程的消息提醒，确保不会造成重复发信。
- 一般情况下，99.9%的几率第一次发信即直接成功，所以在消息推送时，总是在消息推送的前2分钟提前收到消息推送这是正常现象。
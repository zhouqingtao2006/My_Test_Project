# -*- coding:utf-8 -*-
"""
需求：自动读取、执行excel里面的接口测试用例，测试完成后，没返回错误结果并发送邮件通知
一步一步捋清楚需求：
1、设计excel表格
2、读取excel表格
3、拼接url，发送请求
4、汇总错误结果，发送邮件
5、其他注解：
①\n是换行，英文是New line，表示使光标到行首；\r是回车，英文是Carriage return，表示使光标下移一格
"""
import xlrd
import os
import requests
import json
import yaml
import smtplib
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from logging import Logger


def read_case_in_excel(test_case_file):
    test_case_file = os.path.join(os.getcwd(), test_case_file)      # 获取测试用例的路径
    if not os.path.exists(test_case_file):
        Logger().info('测试用例excel文件不存在或路径有误！')
        sys.exit()      # 找不到指定测试文件，就退出程序 os.system("exit")是用来退出cmd的
    test_case = xlrd.open_workbook(test_case_file)      # 读取excel文件
    table = test_case.sheets()[0]       # 获取第一个sheet，下表从0开始
    error_case = []     # 记录错误用例
    '''读取表格中的用例，其实就像一个二维数组'''
    for i in range(1, table.nrows):
        api_id = str(int(table.cell_value(i, 0))).replace("\n", "").replace("\r", "")
        api_name = table.cell_value(i, 1).replace("\n", "").replace("\r", "")
        api_host = table.cell_value(i, 2).replace("\n", "").replace("\r", "")
        api_url = table.cell_value(i, 3).replace("\n", "").replace("\r", "")
        api_method = table.cell_value(i, 4).replace("\n", "").replace("\r", "")
        api_data_type = table.cell_value(i, 5).replace("\n", "").replace("\r", "")
        api_request_data = table.cell_value(i, 6).replace("\n", "").replace("\r", "")
        api_check_point = table.cell_value(i, 7).replace("\n", "").replace("\r", "")
        try:
            # 调用接口请求方法
            status, res = interface_test(api_id, api_name, api_host, api_url, api_method, api_data_type, api_request_data, api_check_point)
            if status != 200:
                # append()只接受一个参数,所以四个参数要用一个括号括起来
                # 请求失败，则向error_case中增加一条记录
                error_case.append((api_id + " " + api_name, str(status), api_host + api_url))
        except Exception as e:
            Logger().error(e)
            Logger().info("第{}个接口请求失败，请检查接口是否异常.".format(api_id))
            # 访问异常，则向error_case中增加一条记录
            error_case.append((api_id + " " + api_name, "请求失败", api_host + api_url))
    return error_case


def interface_test(api_id, api_name, api_host, api_url, api_method, api_data_type, api_request_data, api_check_point):
    # 构造请求头headers
    headers = {
        "Content-Type": "application/json"
    }
    # 判断请求方式，若是GET，调用get请求；若是POST，调用post请求
    if api_method == "GET":
        # 判断get请求是否带参数，然后选择不同get请求方式
        if bool(api_request_data) == False:
            res = requests.get(url=api_host + api_url)
            status_code = res.status_code
            if status_code == 200:
                Logger().info("第{}条用例-{}-执行成功，状态码为:{}，结果返回值为--{}.".format(api_id, api_name, status_code, res.text))
            else:
                Logger().error("第{}条用例-{}-执行失败！！！错误返回码:{}".format(api_id, api_name, status_code))
        else:
            res = requests.get(url=api_host + api_url, params=api_request_data)
            status_code = res.status_code
            if status_code == 200:
                Logger().info("第{}条用例-{}-执行成功，状态码为:{}，结果返回值为--{}.".format(api_id, api_name, status_code, res.text))
            else:
                Logger().error("第{}条用例-{}-执行失败！！！错误返回码:{}".format(api_id, api_name, status_code))
    elif api_method == "POST":
        # 判断api_data_type的类型，选择不同post请求
        if api_data_type == 'Json':
            res = requests.post(url=api_host+api_url, data=api_request_data, headers=headers)
            status_code = res.status_code
            if status_code == 200:
                Logger().info("第{}条用例-{}-执行成功，状态码为:{}，结果返回值为--{}.".format(api_id, api_name, status_code, res.text))
            else:
                Logger().error("第{}条用例-{}-执行失败！！！错误返回码:{}".format(api_id, api_name, status_code))
        else:
            res = requests.post(api_host+api_url, data=json.loads(api_request_data))
            status_code = res.status_code
            if status_code == 200:
                Logger().info("第{}条用例-{}-执行成功，状态码为:{}，结果返回值为--{}.".format(api_id, api_name, status_code, res.text))
            else:
                Logger().error("第{}条用例-{}-执行失败！！！错误返回码:{}".format(api_id, api_name, status_code))
    return status_code, "请求方式错误"


def run_man():
    error_case = test_case_in_excel("API_Case.xlsx")
    if len(error_case) > 0:
        html = '<html><body>接口自动化测试，共有 ' + str(len(error_case)) + ' 个异常接口，列表如下：' + '</p><table><tr><th style="width:100px;text-align:left">接口</th><th style="width:50px;text-align:left">状态</th><th style="width:200px;text-align:left">接口地址</th></tr>'
        for test in error_case:
            html = html + '<tr><td style="text-align:left">' + test[0] + '</td><td style="text-align:left">' + test[1] + '</td><td style="text-align:left">' + test[2] + '</td></tr>'
        send_email(html)
        # print(html)
        with open("report.html", "w") as f:
            f.write(html)
    else:
        Logger().info("本次测试，所有用例全部通过测试")
        send_email("本次测试，所有用例全部通过测试")


# 读取配置文件
def get_conf():
    config_path = os.path.join(os.getcwd(), 'config.yml')
    f = open(config_path, "r", encoding='utf-8')
    cfg = f.read()
    dt = yaml.load(cfg)
    sender = dt['email']['sender']
    recevier = dt['email']['recevier']
    smtpserver = dt['email']['smtpserver']
    username = dt['email']['username']
    password = dt['email']['password']
    return sender, recevier, smtpserver, username, password


# 发送QQ邮件
def send_email(text):
    today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    sender, recevier, smtpserver, username, password = get_conf()
    subject = "[api_test]接口自动化测试结果通知{}".format(today)
    msg = MIMEText(text, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recevier
    try:
        smtp = smtplib.SMTP_SSL(smtpserver, 465)
        smtp.login(sender, password)
        smtp.sendmail(sender, recevier, msg.as_string())
        Logger().info("发送成功")
    except Exception as e:
        Logger().info("发送失败，因为:{}.".format(e))
    # finally:
    #     smtp.quit()


if __name__ == '__main__':
    run_man()



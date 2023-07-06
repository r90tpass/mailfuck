# -*- coding: utf-8 -*-

import json
import time
import pyautogui as pag
import pyperclip
import re
from config.send_config import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from core.set_mails import NameKeyGenerator



def copy_context(file_path, old_link, new_link):
    # 指定 HTML 文件的路径

    # 读取HTML文件内容并替换旧链接为新链接
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace(old_link, new_link)

    # 将替换后的内容覆盖保存到 HTML 文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    # 实例化一个浏览器驱动
    driver = webdriver.Chrome()

    # 使用 file:/// 协议导航到修改后的 HTML 文件
    driver.get(f"file:///{file_path}")

    # 实例化 ActionChains 类
    action = ActionChains(driver)

    # 按下 Ctrl+A 组合键
    action.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()

    # 按下 Ctrl+C 组合键
    action.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()


    # 关闭浏览器
    driver.quit()

def slide_down(coord, distance=2000, duration=0.5):
    pag.moveTo(coord)
    pag.dragTo(coord[0], coord[1] + distance, duration=duration)

def slide_up(coord, distance=200, duration=0.5):
    pag.moveTo(coord)
    pag.dragTo(coord[0], coord[1] - distance, duration=duration)

def auto_new_timed_email_task(receiver_email, subject, mass_single_display, send_time, sender_index, file_path, old_link, new_link):
    pag.moveTo(New_Mail)
    pag.sleep(0.2)
    pag.click()
    time.sleep(0.5)
    if type(receiver_email)==list:
        for i in receiver_email:
            pyperclip.copy(i)  # 复制文本到剪贴板
            pag.sleep(0.2)
            pag.hotkey('ctrl', 'v')  # 粘贴文本到输入框
            pag.sleep(0.2)
            pag.typewrite(' ')  # 输入空格
            pag.sleep(0.2)
    else:
        pyperclip.copy(receiver_email)  # 复制文本到剪贴板
        pag.sleep(0.2)
        pag.hotkey('ctrl', 'v')  # 粘贴文本到输入框
        pag.sleep(0.2)
        pag.typewrite(' ')  # 输入空格
        pag.sleep(0.2)
    
    pag.moveTo(Subject_Name)
    pag.sleep(0.2)
    pag.click()
    pag.sleep(0.2)
    pyperclip.copy(subject)  # 复制文本到剪贴板
    pag.sleep(0.2)
    pag.hotkey('ctrl', 'v')  # 粘贴文本到输入框

    pag.moveTo(Message_body)
    pag.sleep(0.2)
    pag.click()
    pag.sleep(0.2)
    copy_context(file_path, old_link, new_link)
    pag.hotkey('ctrl', 'v')
    pag.sleep(0.2)

    if mass_single_display:
        pag.moveTo(Mass_single_display)
        pag.sleep(0.2)
        pag.click()

    pag.moveTo(Sender_Selection)
    pag.sleep(0.2)
    pag.click()
    time.sleep(0.5)
    #直接滑倒最底部
    # pag.moveTo(move_coord)
    slide_down(paddling_coord)
    if sender_index>10:
        distance = int(sender_index/10)*200
        slide_up(paddling_coord,distance)#滑动200下放出10个新的
        current_sender_coord = Last_to_last_sender[0], Last_to_last_sender[1] - (sender_index%10) * 30
    else:
        current_sender_coord = Last_to_last_sender[0], Last_to_last_sender[1] - sender_index * 30
    pag.moveTo(current_sender_coord)
    pag.sleep(0.2)
    pag.click()

    pag.moveTo(Send_on_time)
    pag.sleep(0.2)
    pag.click()

    pag.moveTo(Send_time)
    pag.click()
    time.sleep(1)
    pag.moveTo(Send_time)
    pag.click()
    time.sleep(1)
    pag.hotkey('ctrl', 'a')
    pag.sleep(0.2)
    pag.press('backspace')
    pag.sleep(0.2)
    pag.typewrite(send_time)
    pag.sleep(0.2)
    pag.press('enter')

    pag.moveTo(Send)
    pag.sleep(0.2)
    pag.click()

def read_and_split_emails(file_path, max_size=3):
    with open(file_path, "r") as file:
        emails = file.readlines()

    # 移除换行符
    emails = [email.strip() for email in emails]

    # 拆分邮件列表，要求每个子列表大小不超过max_size
    split_emails = [emails[i:i + max_size] for i in range(0, len(emails), max_size)]

    return split_emails



def send(mails_file,sel):
    # 从send_mail_config.json文件获取配置信息
    with open('C:\\Users\\Administrator\Desktop\\163fuck\\send\\send_mail_config.json', 'r',  encoding='utf-8') as file:
        config = json.load(file)

    print("将于5秒后开始自动创建定时发送邮件任务，请做好准备。")
    time.sleep(5)
    if sel == 1:
        url = input("请输入你的钓鱼网站的链接eg：https:www.xx.com/index?key  :")
        generator = NameKeyGenerator(mails_file, url)
        mails = generator.generate_name_key_data()
        # 读取文件内容到string变量中，注意这里假定文件在当前目录下
        with open(config["file_path"], 'r', encoding='utf-8') as f:
            string = f.read()

        # 定义正则表达式，匹配类似<a href="https://www.baidu.com/v1HHbjXmV9qS3FboDde8">的标签
        pattern = r"""<div style="text-align: left;">&nbsp;<a [^>]*href="([^"]+)"[^>]*>"""

        # 开始匹配
        matches = re.findall(pattern, string)[0]
        old_link = str(matches)
        sender_index=0
        for i in mails.keys():
            new_link = mails[i]
            # print(f"旧链接是：{old_link}")
            # print(f"新用户是：{i}，新链接是：{new_link}")
            mailslen = len(mails)
            receiver_email=i
            # print(receiver_email)
            # print(config["subject"])
            auto_new_timed_email_task(
                receiver_email,
                subject=config["subject"],
                mass_single_display=config["mass_single_display"],
                send_time=config["send_time"],
                sender_index=sender_index,
                file_path = config["file_path"],
                old_link = str(old_link),
                new_link = str(new_link)
            )
            sender_index+=1
            old_link = new_link
        print("已完成定时发送邮件任务的创建！")     
    elif sel == 0:
        old_link = "http"
        new_link = "http"
        email_lists = read_and_split_emails(mails_file)
        mailslen = len(email_lists)
        for i in range(0,mailslen):
            receiver_email=email_lists[i]
            print(receiver_email)
            auto_new_timed_email_task(
                receiver_email,
                subject=config["subject"],
                mass_single_display=config["mass_single_display"],
                send_time=config["send_time"],
                sender_index=i,
                file_path = config["file_path"],
                old_link = str(old_link),
                new_link = str(new_link)
            )

            print("已完成定时发送邮件任务的创建！")
    else:
        print("不想发算了！！")
    
if __name__ == "__main__":
    mails_file = "C:\\Users\\Administrator\\Desktop\\163fuck\\send\\mails\\100mails.txt"
    sel = int(input("请选择要发送的邮件类型：0单模板，1多模板"))
    send(mails_file,sel)
from config.mv_config import email_coords, sender_name
import time 
import pyautogui as pag
import pyperclip

def batch_modify_sender_name():
    new_sender_name = input("请输入新的统一发件人姓名: ")
    print("将于5秒后开始自动操作，请做好准备。")
    time.sleep(5)

    # 遍历邮箱1-10
    for email_coord in email_coords:
        print(f"现在前往邮箱坐标点{email_coord}")
        pag.moveTo(email_coord) # 邮件1的点
        pag.sleep(0.2)
        pag.click()
        time.sleep(0.5)
        print(f"现在前往邮箱坐标点{sender_name}")
        pag.moveTo(sender_name)
        pag.sleep(0.2)
        pag.click()
        pag.sleep(0.2)
        print(f"现在开始修改发件人姓名")
        # 清除输入框现有的姓名
        pag.hotkey('ctrl', 'a')
        pag.sleep(0.2)
        pag.press('backspace')
        pag.sleep(0.2)
        time.sleep(1)
        # 输入新的发件人姓名
        pyperclip.copy(new_sender_name)  # 复制文本到剪贴板
        pag.sleep(0.2)
        pag.hotkey('ctrl', 'v')  # 粘贴文本到输入框
        pag.sleep(0.2)
        time.sleep(1)
        pag.press('enter')
        time.sleep(2)
    print("好兄弟，这页结束了，翻一下页，保持坐标不变让我们继续")
if __name__ == "__main__":
    # 调用batch_modify_sender_name()函数批量修改发件人姓名
    batch_modify_sender_name()
    print("完成批量修改发件人姓名！")
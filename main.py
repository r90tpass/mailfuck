from core.data_help import notice_input
from core.make_mail import extract_mail
from core.set_add_config import *
from core.auto_mail import *
from core.set_mv_config import *
from core.set_name import *
from core.set_send_config import *
from core.set_send import *
import time 
import threading
import keyboard
import os

# 定义自定义异常类
class ExitProgram(Exception):
    pass


# 监听并处理ESC键按下的函数
def check_esc_key():
    while True:
        if keyboard.is_pressed('esc'):
            print("\n检测到ESC键，准备退出...")
            raise ExitProgram
        time.sleep(0.5)

# 将每个子功能定义为单独的函数
def option_extract_mail():
    extract_mail()

def option_set_addmail_config():
    set_addmail_config()

def option_add_all_mail():
    files = ['data/mail.txt',  'data/mail.csv']
    sel1 = notice_input(['10','20','40','80','100'],'输入单次添加邮箱的最大数量')
    sel2 = notice_input(['0.5s','1s','3s','5s','10s'], '登录等待时间选择（默认选0）(一般默认即可比较快， 网络不好建议选3s以上）')
    print('将网易邮箱大师打开，弄到邮箱设置界面，全屏，再回来命令行选择自动启动倒计时时间')
    sel3 = notice_input(['5s','10s','15s','20s',],'倒计时时间选择(默认0)。\n 启动倒计时后， 迅速切换到网易邮箱大师界面，不动，中间不能动鼠标也不能停止直到执行完毕\n')
    time.sleep((sel3+1)*5)
    mail_df = pd.read_csv(files[1])   
    add_all_mail(mail_df, time_delay=sel2, times=sel1 * 10 + 10)

def option_set_mvname_config():
    set_mvname_config()

def option_batch_modify_sender_name():
    batch_modify_sender_name()

def option_set_send():
    capture_clicks_and_inputs()

def option_send():
    mails_file = "C:\\Users\\Administrator\\Desktop\\163fuck\\send\\mails\\100mails.txt"
    sell = int(input("请选择要发送的邮件类型：0单模板，1多模板"))
    send(mails_file,sell)

# 在单独的线程运行的逻辑
def run_option_thread(cmd):
    option_functions = [option_extract_mail, option_set_addmail_config, option_add_all_mail, option_set_mvname_config, option_batch_modify_sender_name, option_set_send, option_send]
    option = option_functions[cmd]
    option()

# 主要执行逻辑
def main(): 
    choices = [
        '抽取邮箱账户',
        '录制邮箱导入的三个坐标',
        '开始批量导入邮箱',
        '录制修改邮箱发件人的三个坐标',
        '开始批量修改发件人姓名',
        '录制邮箱发送的10个坐标',
        '开始批量定时发送'

    ]   
    
    try:
        # 在后台线程中检查 ESC 键
        esc_thread = threading.Thread(target=check_esc_key, daemon=True)
        esc_thread.start()

        cmd = notice_input(choices)
        
        # 创建和运行选项线程
        option_thread = threading.Thread(target=run_option_thread, args=(cmd, ))
        option_thread.start()
        option_thread.join()
    except ExitProgram:
        print("程序已退出")

    print("完成操作！")

if __name__ == "__main__":
    main()


from core.auto_mail import *
from core.data_help import *

def extract_mail():    
    notice1 = '''
    根据账户账号密码的格式
    输入账号密码列顺序(默认0 1)
    0:邮箱账号
    1:邮箱密码

    例如 邮箱账号:yz94904622@163.com邮箱密码:qh4561416
    则输入 0 1
    回车继续
    '''
    with open('data/mail.txt','r',encoding='utf-8') as f:
        print(f.readline())
    col_name = ['mail_add','mail_pwd']
    columns = input(notice1).strip().split()
    if columns:
        assert(set(columns) == {'0','1'})
        
    else:
        columns = [0,1]
    columns = [col_name[int(i)] for i in columns]

    # 抽取邮箱信息
    df = get_df('data/mail.txt', columns)

    # 保存数据框到csv文件
    csv_file = 'data/mail.csv'
    df.to_csv(csv_file, index=False)
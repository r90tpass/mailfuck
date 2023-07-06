# -*- coding: utf-8 -*-
import time
import pyautogui as pag
from core.data_help import notice_input


def test():
    print('按顺序将鼠标放在邮箱1、发件人姓名、邮箱2处，每次停留10s。\n系统将自动计算邮箱1-10的坐标，以及邮箱1和邮箱10的坐标差，并将结果保存在test_config.py文件中。')

    times = 0
    d = dict()
    ret = []

    try:
        cp = 0
        while True:
            pos = pag.position()
            # 计数鼠标停留在每个坐标上的时间
            if pos in d.keys():
                d[pos] += 1
            else:
                d[pos] = 1

            # 如果某个坐标计数达到10，将其记录下来并执行点击操作
            if d[pos] >= 5:
                print((pos.x, pos.y))
                ret.append((pos.x, pos.y))
                print("坐标已经采集结束下一处")
                d[pos] = -20
                cp += 1

                # 模拟点击已记录的坐标
                pag.click()

                # 在第二个坐标处，模拟输入文字
                if cp == 2:
                    time.sleep(0.1)
                    pag.hotkey('ctrl', 'a')
                    pag.sleep(0.2)
                    pag.press('backspace')
                    pag.sleep(0.2)
                    time.sleep(1)
                    pag.typewrite('test')
                    print("已经采集结束下一个")

            if cp >= 3:
                break
            time.sleep(1)
            times += 1

    except (KeyboardInterrupt, Exception) as e:
        print(e)
        print('发生错误输出停留时间最长的三个坐标，请重新运行。')
        kvs = list(d.items())
        kvs.sort(key=lambda x: x[1])
        kvs.reverse()
        for kv in kvs[:3]:
            ret.append(kv[0].x, kv[0].y)

    # 计算坐标差
    # x_diff = int((ret[2][0] - ret[0][0]))
    y_diff = int((ret[2][1] - ret[0][1]))

    # 计算邮箱1-10的坐标
    email_coords = [ret[0]]
    for i in range(1, 11):
        email_coords.append((ret[0][0], ret[0][1] + y_diff * i))

    # 将计算结果写入test_config.py文件
    with open('test_config.py', 'w') as f:
        f.write("email_coords = [\n")
        for coord in email_coords:
            f.write(f"    ({coord[0]}, {coord[1]}),\n")
        f.write("]\n")
        f.write(f"sender_name = ({ret[1][0]}, {ret[1][1]})\n")
        f.write(f"email1_to_email10_diff = (0, {y_diff})\n")

    print("配置完成，已保存到test_config.py文件中。")

    return email_coords, ret[1], ret[2], (0, y_diff)

def set_mvname_config():
    sel = notice_input(['不录制', '录制'], '是否要录制邮箱1-10和发件人姓名的坐标')
    if sel == 1:
        email_coords, sender_name, email11, email1_to_email10_diff = test()
        print("完成配置!")
        print("邮箱1-11坐标:", email_coords)
        print("发件人姓名坐标:", sender_name)
        print("第11个邮箱的坐标是",email11)
        print("邮箱1到邮箱10坐标差:", email1_to_email10_diff)
if __name__ == "__main__":
    set_mvname_config()
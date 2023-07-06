import time
import pyautogui as pag

def capture_clicks_and_inputs():
    print('请在依次在9个指定位置停留10s，程序会自动记录坐标点并在2、4、5、6号点进行不同的输入。')
    times = 0
    d = dict()
    ret = []

    try:
        cp = 0
        input_points = {1: ["11@11.com","22@22.com",'123123@163.com'], 3: "teststt", 4: "tstettss", 9: "20:00"}  # 在指定的坐标点进行输入
        while True:
            pos = pag.position()
            
            # 计数鼠标停留在每个坐标上的时间
            if pos in d.keys():
                d[pos] += 1
            else:
                d[pos] = 1
              
            # 如果某个坐标计数达到5，将其记录下来并执行点击操作
            if d[pos] >= 5:
                ret.append((pos.x, pos.y))
                print(f"坐标已记录{(pos.x, pos.y)}")
                d[pos] = -20
                cp += 1
                # 模拟点击已记录的坐标
                pag.click()
                time.sleep(1)

                # 在指定的坐标点进行输入
                if cp in input_points:
                    if cp == 1:
                        for i in input_points[cp]:
                            pag.typewrite(i)
                            pag.sleep(0.2)
                            pag.typewrite(' ')  # 输入空格
                            pag.sleep(0.2)
                    elif cp == 9:
                        pag.click()
                        time.sleep(1)
                        pag.hotkey('ctrl', 'a')
                        pag.sleep(0.2)
                        pag.press('backspace')
                        pag.sleep(0.2)
                        pag.typewrite(input_points[cp])
                        pag.sleep(0.2)
                    else:
                        pag.typewrite(input_points[cp])
                        pag.sleep(0.2)

            if cp >= 10:
                break
            time.sleep(1)
            times += 1
            
    except (KeyboardInterrupt, Exception) as e:
        print(e)
        print('发生错误, 请重新运行。')
        
    else:
        #将计算结果写入send_config.py文件
        with open('C:\\Users\\Administrator\\Desktop\\163fuck\\config\\send_config.py', 'w') as f:
            coord_names = [
                "New_Mail",
                "Mass_single_display",
                "Subject_Name",
                "Message_body",
                "Sender_Selection",
                "paddling_coord",
                "Last_to_last_sender",
                "Send_on_time",
                "Send_time",
                "Send"
            ]
            for i in range(0,len(coord_names)):
                f.write(f"{coord_names[i]} = {ret[i]}\n")
            print("配置完成，已保存到send_config.py文件中。")

    return ret

if __name__ == "__main__":
    # 调用capture_clicks_and_inputs()函数记录坐标点并执行输入操作
    capture_clicks_and_inputs()
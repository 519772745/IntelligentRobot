from ultrasonic import ultrasonic
from infrared import infrared
from line_tracker import line_tracker
import time

# Chinese comments are just for my own to understand the code
address="192.168.0.101"  #定义了IP，就是机器人的IP地址

inf=infrared(address)
inf.start()
ult=ultrasonic(address)
ult.start()
lt=line_tracker(address) 

from motor import motor
mot=motor(address)


lt.start() #开启了灰度传感器
inf_t=time.time()
thr=350 #这是灰度传感器的值，数值越小表示越黑
temp=0

while True:
    try:
        t=time.time()
        if t-inf_t>1:  #在开始执行之后
            print("line_tracker: ",lt.data)

            if lt.data[2]<thr:
                mot.command("forward",5,0.3) #马达前进，机器人前进；数值为前进速度和时间
                print("Forward")
            else:
                if lt.data[1]<thr or lt.data[0]<thr:
                    mot.command("left",0.25,0.5)
                    print ("Left")
                elif lt.data[3]<thr or lt.data[4]<thr:
                    mot.command("right",0.25,0.5)
                    print ("Right")
                else:
                    mot.command("set_left_speed",4,0.6) #开始转
                    mot.command("set_right_speed",4,0.6)
                    mot.command("left")
                    time.sleep(2)
                    print("trun")
                    continue
            inf_t=t

    except KeyboardInterrupt:
        inf.stop()
        ult.stop()
        lt.stop()
        mot.stop()
        break

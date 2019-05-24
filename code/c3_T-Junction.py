# from ultrasonic import ultrasonic
# from infrared import infrared
from line_tracker import line_tracker
import time
address="192.168.0.101"
# inf=infrared(address)
# inf.start()
# ult=ultrasonic(address)
# ult.start()
lt=line_tracker(address)
from motor import motor
from time import sleep
mot=motor(address)
lt.start()
# inf_t=time.time()
# maxs = [648,660,609,695,605]
# mins = [217,247,237,235,204]
# thr = [(a+b)/2 for a,b in zip(maxs,mins)]
thr=350

while True:
    try:
        #rota=-1
        # t=time.time()
        # if t-inf_t>1:
        print("line_tracker: ",lt.data)
        if type(lt.data) == int:
            continue
        num=[0,0,0,0,0]
        for i in range(5):
            if lt.data[i] < thr:
                num[i] = 1
            else:
                num[i] = 0
        print(num)



        def get_num():   #get data
            for i in range(5):
                if lt.data[i] < thr:
                    num[i] = 1
                else:
                    num[i] = 0
            return;

        def one_step():         #when cross go one little step
            motor.command("forward",3,0.5)
            print("one step")
            return;

        def Strignt():          #go straight
            get_num()
            if num==[0,0,1,0,0]:
                mot.command("forward",3)
                print ("forward")
            elif num==[1,0,0,0,0]:
                mot.command("set_left_speed",1)
                mot.command("set_right_speed", 3)
                mot.command("forward")
                print ("forward")
            elif num==[0,1,0,0,0]:
                mot.command("set_left_speed",1)
                mot.command("set_right_speed", 2)
                mot.command("forward")
                print ("forward")
            elif num==[1,1,0,0,0]:
                mot.command("set_left_speed",1)
                mot.command("set_right_speed", 2)
                mot.command("forward")
                print ("forward")
            elif num==[0,1,1,0,0]:
                mot.command("set_left_speed",1)
                mot.command("set_right_speed", 2)
                mot.command("forward")
                print ("forward")
            elif num==[0,0,0,0,1]:
                mot.command("set_left_speed",3)
                mot.command("set_right_speed", 1)
                mot.command("forward")
                print ("forward")
            elif num==[0,0,0,1,0]:
                mot.command("set_left_speed",2)
                mot.command("set_right_speed", 1)
                mot.command("forward")
                print ("forward")
            elif num==[0,0,0,1,1]:
                mot.command("set_left_speed",2)
                mot.command("set_right_speed", 1)
                mot.command("forward")
                print ("forward")
            elif num==[0,0,1,1,0]:
                mot.command("set_left_speed",2)
                mot.command("set_right_speed", 1)
                mot.command("forward")
                print ("forward")
            else:
                mot.command("forward",3)
                print ("forward")
            sleep(0.1)
            return;

        def U_back():           # go back

            while True:
                get_num()
                mot.command("set_left_speed", 0, 0.4)
                mot.command("set_right_speed", 10, 0.4)
                mot.command("left")
                if num==[0,0,1,0,0] or num==[0,1,1,0,0] or num==[0,0,1,1,0] or num==[0,1,0,0,0] or num==[0,0,0,1,0]:
                    break
            print ("Trun back")
            return;

        def Left():# go left 90°
            while True:
                get_num()
                mot.command("set_left_speed", 0, 0.3)
                mot.command("set_right_speed", 10, 0.3)
                mot.command("left")
                if num==[0,0,1,0,0]:
                    break
            print ("Trun left")
            return;

        def Right(): # go right 90°
            while True:
                get_num()
                mot.command("set_left_speed", 10, 0.3)
                mot.command("set_right_speed", 0, 0.3)
                mot.command("right")
                if num==[0,0,1,0,0]:
                    break
            print ("Trun right")
            return;

        def Stop():           # stop
            mot.command("set_left_speed", 0)
            mot.command("set_right_speed", 0)
            print ("Stop")
            return;





        def cross():
            if num==[1,1,1,1,1]:
                one_step()
                if num==[1,1,1,1,1]:     #arrive the end
                    time.sleep(5)

                elif num==[0,0,1,0,0]:     # cross type
                    mot.command("set_left_speed", 6)
                    mot.command("set_right_speed", 4)
                    mot.command("left")
                    print("left")
                elif num==[0,0,0,0,0]:      # T type
                    mot.command("set_left_speed", 6)
                    mot.command("set_right_speed", 4)
                    mot.command("left")
                    print("left")


    except KeyboardInterrupt:
        break
lt.stop()
mot.stop()
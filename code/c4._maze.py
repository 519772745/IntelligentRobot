# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:14:25 2019

@author: Sun Yixuan,Chen Mengxuan,Li Yutong
"""
import time
from ultrasonic import ultrasonic
from infrared import infrared
from line_tracker import line_tracker
# Chinese comments are just for my own to understand the code

address="192.168.0.106"  #定义了IP，就是机器人的IP地址
inf=infrared(address)
inf.start()
ult=ultrasonic(address)
ult.start()
lt=line_tracker(address) #这个line_tracker是啥，还需要看。py引包还不太熟
lt.start() #开启了灰度传感器
time.sleep(1)
print(lt.data)
thr=350 #这是灰度传感器的值，数值越小表示越黑
from motor import motor
mot=motor(address)

direction_stack=[]

def has_reached():
    print('has_reached')
    """ hasreached()   
    Features:用于验证机器人是否到达终点
             Verify weather the robot has reached the end

    Args: None
        
    Returns:
        false: 机器人未到达终点
              the robot has't reached the end.
        true: 机器人到达了终点
              the robot has't reached the end.
    """
    r_has_reached()

def turn(direction):
    print('turn')
    """ turn
    Features:让机器人沿某个方向(左/右)转90°
             Let the robot rotate 90 degrees in one direction(left or right)
             

    Args: direction 方向
        
    Returns:None
    """
    if (direction =="left"):
        turn_left()
    else:
        turn_right()

def go_forward(direction):
    print('go_forward')
    """ go_forward
    Features:让机器人前进或后退
             Let the robot move forward or backward
             
    Args: direction 方向
        
    Returns:None
    """
    if(direction=="forward"):
        r_go_forward()
    else:
        r_go_backward()
        
        
def try_to_move(direction):
    print('try_to_move')
    print(direction)
    """ try_to_move   
    Features:让机器人沿着给定方向前进一段距离。
             移动后，若机器人发现已经偏离黑线，则返回原点。
             若可以沿此方向移动，则将移动的方向录入方向栈。
             Let the robot move a certain distance along a given direction.
             After moving, if the robot finds that it has deviated from the black line, 
             it will return to the origin.
             If the robot can move in this direction, the direction will be entered in the direction stack.
             

    Args: direction 方向
          direction_stack 方向栈
        
    Returns:
        false: 机器人不可以往这个方向前进
              the robot can't move in this direction
        true: 机器人可以，并且已经往这个方向前进了
              The robot can, and has moved in this direction.
    """
    global direction_stack
   
    #判断是否转弯
    if(direction!="forward"):   #如果不是前进，则让它先转向再前进
        if(can_turn(direction)):
            turn(direction)  #先转弯
        else: #不可以转弯返回False
            return False
    
    #把方向泵入栈
    direction_stack.append(direction)  #栈入方向
    print (direction_stack)
    
    #前进
    r_go_forward()
    
    if no_way():  #判断前方是否有路
        r_go_backward()
        return False
    else:
        return True

def back_to_origin():
    print('back_to_origin')
    """ back_to_origin   
    Features:让机器人回到原点(即回退一步)
             Let the robot return back to the origin(Take a step back)
             

    Args: direction_stack 方向栈
        
    Returns:None
    """
    global direction_stack
    length=len(direction_stack)
    direction=direction_stack.pop(length-1)
    
    r_go_backward()          #TODO 这里转回去应该是向左向右转
    if(direction=="left"):
        turn("right")
    if(direction=="right"):
        turn("left")
        

def move(direction):
    """ move
    Features:递归的方法，让机器人搜索可前进的路径。并把正确的路径保存在栈(direction_stack)中
             A recursive approach that lets the robot search for paths that can go forward. 
             And save the correct path in the stack (direction_stack)
             

    Args: direction 方向
        
    Returns:False 该方向错误
            True 该方向正确
    """
    if has_reached():
        print("=============================================")
        print("              已到达终点")
        print("=============================================")
        return True
    else:
        if try_to_move(direction):
            if move("forward"):
                return True
            elif move("left"):
                return True
            elif move("right"):
                return True
            else:
                back_to_origin()
                return False
        else:
            return False   #即如果不能走的话，返回false
    return False
        
def move_again():
    """ move_again
        Let the robot move again w(ﾟДﾟ)w
    """
    global direction_stack
    turn_left()
    turn_left()
    length=len(direction_stack)
    for i in range(len):
        direction=direction_stack[length-1-i]
        if direction=="forward":
            go_forward()
        elif direction=="left":
            turn_right()
            go_forward()
        else:
            turn_left()
            go_forward()  
    


    
#停止驱动的代码
def stop():
    inf.stop()
    ult.stop()
    lt.stop()
    mot.stop()


        
        
#直行        
def r_go_forward(max_time=3): 
    print('r_go_forward')
    i=1
    while True:
        try:
            print("line_tracker: ",lt.data)
            #reading = lt.data
            #reading[0] == thr
            print("i",i)
            if lt.data[2]<thr:
                mot.command("forward",0.1,0.3) #马达前进，机器人前进；数值为前进速度和时间
                print("Forward")
                i=i-1
            else:
                if lt.data[1]<thr and lt.data[0]>thr:
                    mot.command("left",0.1,0.5)

                    print ("Left")
                elif lt.data[3]<thr and lt.data[4]>thr:
                    mot.command("right",0.1,0.5)
                    print ("Right")
                else:
                    mot.command("forward", 0.1, 0.3) #TODO 这里写成暂停会比较好
                    i=i-1
            time.sleep(0.1)
            if(i==0):
                break
        except KeyboardInterrupt:
            break
 
#后退    
def r_go_backward(max_time=3):
    print('r_go_backward')
    i=1
    while True:
        try:
            print("line_tracker: ",lt.data)
    
            if lt.data[2]<thr:
                mot.command("backward",0.1,0.3) #马达前进，机器人前进；数值为前进速度和时间
                print("Backward")
                i=i-1
            else:
                if lt.data[1]<thr and lt.data[0]>thr:
                    mot.command("right",0.1,0.5)
                    
                    print ("Right")
                elif lt.data[3]<thr and lt.data[4]>thr:
                    mot.command("left",0.1,0.5)
                    
                    print ("Left")
                else:
                    mot.command("backward", 1, 0.3) #TODO 这里写成暂停会比较好
                    i=i-1
            time.sleep(0.1)
            if i==0:
                break
            
        except KeyboardInterrupt:
            pass
        
def turn_left():
    print('turn_left')
    mot.command("set_left_speed",4)
    mot.command("set_right_speed",4)
    mot.command("left") 
    time.sleep(0.1)
    print ("turn_left")
    
def turn_right():
    print('turn_right')
    mot.command("set_left_speed",4)
    mot.command("set_right_speed",4)
    mot.command("right")
    time.sleep(0.1)
    print ("turn_right")
    
def r_has_reached():
    print('r_has_reached')
    if lt.data[0] < thr and lt.data[1] < thr and lt.data[2] < thr and lt.data[3] < thr and lt.data[4] < thr:
         r_go_forward()
         if lt.data[0] < thr and lt.data[1] < thr and lt.data[2] < thr and lt.data[3] < thr and lt.data[4] < thr:
             return True  #到达了终点
         else:
            r_go_backward()
            return False
    else:
        return False
   
def no_way():
    data=lt.data
    if data[1] > thr and data[2] > thr and data[3] > thr:
        return True
    return False

def can_turn(direction):
    print("can_turn")
    if (direction =="right"):
        if lt.data[3] < thr and lt.data[4] < thr:
            return True
        else: 
            return False
    else:
        if lt.data[0] < thr and lt.data[1]:
            return True
        else:
            return False
def return_true():
    return True
		
try:
    move("forward")
    print("开始")
    print("最终路径:",direction_stack)

except KeyboardInterrupt:
    stop()
    return_true()
		
		
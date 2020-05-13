"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import random

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  >= (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 < (pred) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
    
    def get_side_pred():
        x = (240 - scene_info["ball"][1]) // scene_info["ball_speed"][1]
        ball_y = scene_info["ball_speed"][1]*x
    #找出frame在frame_begin時的ballx位置，blocker位置，和他們的x方向
        ball_x = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) #ball位置
        ball_x_speed = scene_info["ball_speed"][0]                     #ball方向
        if scene_info["ball_speed"][0]>0 and ball_x >=195:
            ball_x_speed = -scene_info["ball_speed"][0]    #到達y_begin時球方向往左
        elif scene_info["ball_speed"][0]>0 and ball_x <195:
            ball_x_speed = scene_info["ball_speed"][0]     #到達y_begin時球方向往右
        elif scene_info["ball_speed"][0]<0 and ball_x >0:
            ball_x_speed = scene_info["ball_speed"][0]    #到達y_begin時球方向往左
        else:
            ball_x_speed = -scene_info["ball_speed"][0]     #到達y_begin時球方向往右
        if (ball_x - 195) // scene_info["ball_speed"][0] > 0 and (ball_x - 195)>0:
            modify_R = (ball_x-195) % scene_info["ball_speed"][0]
        else:
            modify_R = 0    
        if (ball_x-0) // scene_info["ball_speed"][0] > 0 and (ball_x-0)>0:
            modify_L = (ball_x-0) % scene_info["ball_speed"][0]
        else:
            modify_L = 0
        if ball_x > 195:    
            ball_x = 195 - (ball_x - 195)
            ball_x = ball_x + modify_R
        elif ball_x < 0:
            ball_x = -(ball_x)
            ball_x = ball_x - modify_L

        blocker_x = scene_info["blocker"][0]+3*direction*x #blocker位置
        blocker_x_speed = 3*direction            #blocker方向
        if direction==1 and blocker_x >=170:
            blocker_x_speed = -blocker_x_speed    #到達y_begin時球方向往左
        elif direction==1 and blocker_x <170:
            blocker_x_speed = blocker_x_speed   #到達y_begin時球方向往右
        elif direction==(-1) and blocker_x >0:
            blocker_x_speed = blocker_x_speed    #到達y_begin時球方向往左
        else:
            blocker_x_speed = -blocker_x_speed     #到達y_begin時球方向往右
        if (blocker_x - 170) // 3*direction > 0 and (blocker_x - 170)>0:
            modify_R = (blocker_x-170) % 3*direction
        else:
            modify_R = 0    
        if (blocker_x-0) // 3*direction > 0 and (blocker_x-0)>0:
            modify_L = (blocker_x-0) % 3*direction
        else:
            modify_L = 0
        if blocker_x > 170:    
            blocker_x = 170 - (blocker_x - 170)
            blocker_x = blocker_x + modify_R
        elif blocker_x < 0:
            blocker_x = -(blocker_x)
            blocker_x = blocker_x - modify_L

        if blocker_x_speed > 0 and ball_x_speed < 0:
            if blocker_x < ball_x and (blocker_x+blocker_x_speed) >= (ball_x+ball_x_speed) and (ball_y+ball_x_speed) >=240:
                ball_x = blocker_x+blocker_x_speed
                ball_x_speed = -ball_x_speed
            else:
                return -1
        elif blocker_x_speed < 0 and ball_x_speed > 0:
            if blocker_x > ball_x and (blocker_x+blocker_x_speed) <= (ball_x+ball_x_speed) and (ball_y+ball_x_speed) >=240:
                ball_x = blocker_x+blocker_x_speed
                ball_x_speed = -ball_x_speed
            else:
                return -1

        #預測落點
        x = (415 - ball_y) // abs(ball_x_speed)
        mod = (415 - ball_y) % abs(ball_x_speed)
        if mod != 0:
            x = x + 1
        pred = ball_x+(ball_x_speed*x)
        if (pred - 195) // ball_x_speed > 0 and (pred - 195)>0:
            modify_R = (pred-195) % ball_x_speed
        else:
            modify_R = 0
        if (pred-0) // ball_x_speed > 0 and (pred-0)>0:
            modify_L = (pred-0) % ball_x_speed
        else:
            modify_L = 0
        if pred > 195:
            pred = 195 - (pred - 195)
            pred = pred + modify_R
        elif pred < 0:
            pred = -(pred)
            pred = pred - modify_L
            print("pred",pred)
        return pred


    def get_bound_pred():
                ball_NowspeedY = -(scene_info["ball_speed"][1])
                x = (scene_info["ball"][1] - 260) // ball_NowspeedY #幾個frame以後會需要碰到障礙物
                mod = (scene_info["ball"][1] - 260) % ball_NowspeedY
                if mod != 0:
                    x = x + 1
                pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測到達板子的位置
                if scene_info["ball_speed"][0]>0 and pred >=195:
                    ball_thenSpeed = -scene_info["ball_speed"][0]    #打到板子時球方向往左
                elif scene_info["ball_speed"][0]>0 and pred <195:
                    ball_thenSpeed = scene_info["ball_speed"][0]     #打到板子時球方向往右
                elif scene_info["ball_speed"][0]<0 and pred >0:
                    ball_thenSpeed = scene_info["ball_speed"][0]    #打到板子時球方向往左
                else:
                    ball_thenSpeed = -scene_info["ball_speed"][0]     #打到板子時球方向往右
                if (pred - 195) > 0 and (pred - 195) % scene_info["ball_speed"][0] !=0:
                    modify_R = (195-pred) % scene_info["ball_speed"][0]
                else:
                    modify_R = 0    
                if (pred - 0) <0 and (pred - 0) % scene_info["ball_speed"][0] !=0:
                    modify_L = (pred-0) % scene_info["ball_speed"][0]
                else:
                    modify_L = 0
                if pred > 195:    
                    pred = 195 - (pred - 195)
                    pred = pred + modify_R
                elif pred < 0:
                    pred = -(pred)
                    pred = pred - modify_L
            
                pred_415 = pred+(ball_thenSpeed*x)
                if (pred - 195) >0 and (pred - 195) % ball_thenSpeed != 0:
                    modify_R = (pred-195) % ball_thenSpeed
                else:
                    modify_R = 0
                if (pred - 0) <0 and (pred - 0) % ball_thenSpeed != 0:
                    modify_L = (pred-0) % ball_thenSpeed
                else:
                    modify_L = 0
                if pred_415 > 195:
                    pred_415 = 195 - (pred_415 - 195)
                    pred_415 = pred_415 + modify_R
                elif pred_415 < 0:
                    pred_415 = -(pred_415)
                    pred_415 = pred_415 - modify_L
                print("pred",pred_415)
                return pred_415

    def ml_loop_for_1P(): 
        if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
            pred_b = get_side_pred()
            x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            bound = pred // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 == 1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            
            return move_to(player = '1P',pred = pred)
        else : # 球正在向上 # ball goed up  
            pred = get_bound_pred() 
            if scene_info["ball"][1] >= 415:
                print("actual",scene_info["ball"][0]) 
            if scene_info["ball"][1] >= 150:
                return move_to(player = '1P',pred = pred)
            else:
                return move_to(player = '1P',pred = 100)



    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    direction = 100
    blocker_pre = 100
    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information
        if scene_info["frame"] == 1:
            blocker_pre = scene_info["blocker"][0]
        else:
            if blocker_pre < scene_info["blocker"][0]:
                direction = 1
            else:
                direction = -1
            blocker_pre = scene_info["blocker"][0]

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            if side == "1P":
                command = ml_loop_for_1P()
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            

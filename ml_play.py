"""
The template of the main script of the machine learning process
"""
import pickle
from os import path

import numpy as np
import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)



def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    filename = path.join(path.dirname(__file__), 'save','clf_KMeans_BallAndDirection.pickle')
    with open(filename, 'rb') as file:
        clf = pickle.load(file)
    s = [95, 400]
    v_pre = [0, 0]
    def get_direction(ball_x, ball_y, ball_pre_x, ball_pre_y):
        VectorX = ball_x - ball_pre_x
        VectorY = ball_y - ball_pre_y
        if (VectorX == 0 and VectorY == 0):
            return 0
        elif (VectorX == 0 and VectorY > 0):
            return 1
        elif (VectorX == 0 and VectorY < 0):
            return 2
        elif (VectorX > 0 and VectorY == 0):
            return 3
        elif (VectorX < 0 and VectorY == 0):
            return 4
        elif (VectorX > 0 and VectorY > 0):
            return 5
        elif (VectorX > 0 and VectorY < 0):
            return 6
        elif (VectorX < 0 and VectorY > 0):
            return 7
        elif (VectorX < 0 and VectorY < 0):
            return 8


    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        feature = []
        vectorX = scene_info.ball[0] - s[0]
        vectorY = scene_info.ball[1] - s[1]
    
        feature.append(scene_info.ball[0])
        feature.append(scene_info.ball[1])
        feature.append(vectorX)
        feature.append(vectorY)
        feature.append(get_direction(scene_info.ball[0], scene_info.ball[1], s[0], s[1]))

        if(vectorX*v_pre[0] < 0) and (vectorY*v_pre[1] < 0):
            if(v_pre[0]>0) and (v_pre[1]>0):
                feature.append(1)
            elif(v_pre[0]>0) and (v_pre[1]<0):
                feature.append(2)
            elif(v_pre[0]<0) and (v_pre[1]>0):
                feature.append(3)
            else:
                feature.append(4)
        elif(vectorX*v_pre[0] < 0):    
            if(v_pre[0]>0):
                feature.append(5)
            else:
                feature.append(6)
        elif(vectorY*v_pre[1] < 0):    
            if(v_pre[1]>0):
                feature.append(7)
            else:
                feature.append(8)
        else:
            feature.append(0)

        s = [scene_info.ball[0], scene_info.ball[1]]
        v_pre = [vectorX, vectorY]
        feature = np.array(feature)
        feature = feature.reshape((1,-1))
        print(feature)
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
                
            y = clf.predict(feature)
            
            if y == 0:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                print('NONE')
            elif y == 1:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                print('LEFT')
            elif y == 2:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                print('RIGHT')

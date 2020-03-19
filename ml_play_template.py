"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( 
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
    count = 0
    list1 = [(93, 395),
    (98, 395),
(14, 395),
(127, 395),
(167, 395),
(54, 395),
(42, 395),
(155, 395),
(125, 395),
(127, 395),
(125, 395),
(102, 395),
(181, 395),
(68, 395),
(42, 395),
(65, 395),
(84, 395),
(167, 395),
(158, 395),
(86, 395),
(91, 395),
(90, 395),
(105, 395),
(6, 395),
(174, 395),
(165, 395),
(146, 395),
(147, 395),
(161, 395),
(175, 395),
(189, 395),
(188, 395),
(174, 395),
(160, 395),
(146, 395),
(132, 395),
(42, 395),
(42, 395),
(34, 395),
(90, 395),
(7, 395),
(63, 395),
(20, 395),
(93,395),
(173,395)]
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

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
        if scene_info.platform[0]+20 < list1[count][0]-6:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif scene_info.platform[0]+20 > list1[count][0]+6:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
             comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        if scene_info.ball[1]>=395:    
            count += 1
        if scene_info.ball[1] >=395:
            print(scene_info.ball)
        
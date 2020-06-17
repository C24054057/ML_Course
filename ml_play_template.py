class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"


        a = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        min = 10000

        #  1  2  3    
        #  4  5  6   
        #  7  8  9
        #每格為76 X 80
        #假設我的車子在8

        car1 = car2 = car3 = car4 = car5 = False
        car6 = car7 = car8 = car9 = False

        intervalx = 70
        intervaly = 100
        if scene_info["frame"] > 0 and scene_info[self.player]:
            square8 = [scene_info[self.player][0], scene_info[self.player][1]]
            square5 = [square8[0], square8[1]-intervaly]
            square2 = [square8[0], square8[1]-2*intervaly]
            square7 = [square8[0]-intervalx, square8[1]]
            square4 = [square8[0]-intervalx, square8[1]-intervaly]
            square1 = [square8[0]-intervalx, square8[1]-2*intervaly]
            square9 = [square8[0]+intervalx, square8[1]]
            square6 = [square8[0]+intervalx, square8[1]-intervaly]
            square3 = [square8[0]+intervalx, square8[1]-2*intervaly]
            #每個區塊裡有沒有車，true代表有車子
            for car in scene_info["cars_info"]:
                if car['pos'][0] >= square1[0] - intervalx/2 and car['pos'][0] <= square1[0] + intervalx/2 and \
                    car['pos'][1] >= square1[1] - intervaly/2 and car['pos'][1] <= square1[1] + intervaly/2:
                    car1 = True
                if car['pos'][0] >= square2[0] - intervalx/2 and car['pos'][0] <= square2[0] + intervalx/2 and \
                    car['pos'][1] >= square2[1] - intervaly/2 and car['pos'][1] <= square2[1] + intervaly/2: 
                    car2 = True 
                if car['pos'][0] >= square3[0] - intervalx/2 and car['pos'][0] <= square3[0] + intervalx/2 and \
                    car['pos'][1] >= square3[1] - intervaly/2 and car['pos'][1] <= square3[1] + intervaly/2:
                    car3 = True
                if car['pos'][0] >= square4[0] - intervalx/2 and car['pos'][0] <= square4[0] + intervalx/2 and \
                    car['pos'][1] >= square4[1] - intervaly/2 and car['pos'][1] <= square4[1] + intervaly/2: 
                    car4 = True
                if car['pos'][0] >= square5[0] - intervalx/2 and car['pos'][0] <= square5[0] + intervalx/2 and \
                    car['pos'][1] >= square5[1] - intervaly/2 and car['pos'][1] <= square5[1] + intervaly/2:
                    car5 = True
                if car['pos'][0] >= square6[0] - intervalx/2 and car['pos'][0] <= square6[0] + intervalx/2 and \
                    car['pos'][1] >= square6[1] - intervaly/2 and car['pos'][1] <= square6[1] + intervaly/2: 
                    car6 = True
                if car['pos'][0] >= square7[0] - intervalx/2 and car['pos'][0] <= square7[0] + intervalx/2 and \
                    car['pos'][1] >= square7[1] - intervaly/2 and car['pos'][1] <= square7[1] + intervaly/2:
                    car7 = True
                if car['pos'][0] >= square8[0] - intervalx/2 and car['pos'][0] <= square8[0] + intervalx/2 and \
                    car['pos'][1] >= square8[1] - intervaly/2 and car['pos'][1] <= square8[1] + intervaly/2: 
                    car8 = True
                if car['pos'][0] >= square9[0] - intervalx/2 and car['pos'][0] <= square9[0] + intervalx/2 and \
                    car['pos'][1] >= square9[1] - intervaly/2 and car['pos'][1] <= square9[1] + intervaly/2:
                    car9 = True
            if car2 == True or car5 == True:
                if car9 == True:
                    return ["MOVE_LEFT", "SPEED"]
                elif car7 == True:
                    return ["MOVE_RIGHT", "SPEED"]
                elif car6 == True:
                    return ["MOVE_LEFT", "SPEED"]
                elif car4 == True:
                    return ["MOVE_RIGHT", "SPEED"]
                elif square8[0] > 317:
                    return ["MOVE_LEFT", "SPEED"]
                else:
                    return ["MOVE_RIGHT", "SPEED"]
            else:
                for i in range(9):
                    temp = a[i] - square8[0]
                    if abs(temp) < abs(min):
                        min = temp
                if min < -5:
                    return ["MOVE_LEFT", "SPEED"]
                elif min > 5:
                    return ["MOVE_RIGHT", "SPEED"]
                else:
                    return ["SPEED"]
                               
        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        
        pass

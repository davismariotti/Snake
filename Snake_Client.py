'''
Created on Jan 7, 2013

@author: gomeow
'''
from PodSixNet.Connection import connection, ConnectionListener
import threading, time, pygame, random, urllib2, sys

global t1, t2, ready, pos, c, dir_x2, dir_y2, x2, y2, which, new, food1, food2, death2
ready = False
pos = 0
food1 = 0
food2_ = 0
which = 0
new = 0
c = 0
death2 = False
class Client(ConnectionListener):
    global players, ready, pos
    players = []
    def getPlayers(self):
        return self.players
    def __init__(self, host, port):
        self.Connect((host, port))

        nick = "Anonymous"
        connection.Send({"action": "nickname", "nickname": nick})

    def Loop(self):
        connection.Pump()
        self.Pump()
    def sendData(self, data):
        connection.Send(data)
    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_players(self, data):
        global players
        # Recieved list of players.
    def Network_connected(self, data):
        print "You are now connected to the server"
    def Network_ready(self, data):
        global ready, pos, food1, food2_
        ready = True
        pos = data['pos']
        food1 = data['food1']
        food2_ = data['food2']

    def Network_loc(self, data):
        global x2, y2, dir_x2, dir_y2
        print data
        x2 = data['loc'][0]
        y2 = data['loc'][1]
        dir_x2 = data['dir'][0]
        dir_y2 = data['dir'][1]

    def Network_food(self, data):
        global which, new
        print data
        which = data['which']
        new = data['new']
    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()
    def Network_death(self, data):
        global death2
        print data
        death2 = True
    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()
def startClient():
    global c
    while 1:
        # Try except stops exception when quitting
        try:
            c.Loop()
            time.sleep(0.001)
        except:
            pass
def connect():
    setupMusics()
    global c, t1, t2
    c = Client("localhost", 12345)
    t1 = threading.Thread(target=startClient)
    t1.start()
    #t1.join()
    t2 = threading.Thread(target=start)
    t2.start()
    t2.join()
    
def setupMusics():
    f = open("tetris.mid", "wb")
    f.write(urllib2.urlopen("http://gomeow.info/files/tetrisb.mid").read())
    f.close()
    pygame.mixer.init()
    pygame.mixer.music.load("tetris.mid")
    pygame.mixer.music.play(-1)
def start():
    pygame.init()
    global death2, dir_x, dir_y, dir_x2, dir_y2, ready, pos, x, y, x2, y2, c, which, new, food1, food2
    width = 640
    height = 400
    x = 0
    y = height/2 
    x2 = 0
    y2 = height/2
    dir_x = 0
    dir_y = -1
    dir_x2 = 0
    dir_y2 = -1
    screen = pygame.display.set_mode((width, height))
    BLACK = (0, 0, 0)
    clock = pygame.time.Clock()
    class Food:
        def __init__(self, s, x, y, h):
            self.screen = s
            self.x = x
            self.y = y
            self.foodheight = h
            self.eaten = False
            self.who = 0
        def draw(self):
            pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.foodheight, self.foodheight))
        def setEaten(self, eaten, who):
            self.eaten = eaten
            self.who = who
        def getWho(self):
            return self.who
        def isEaten(self):
            return self.eaten
        def didHit(self, point):
            if point[0] < self.x or point[0] > self.x + self.foodheight:
                return False
            elif point[1] < self.y or point[1] > self.y + self.foodheight:
                return False
            else:
                return True
    def getRand():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def do():
        global death2, ready, pos, dir_x, dir_y, dir_x2, dir_y2, x, y, x2, y2, c, which, new, food1, food2
        points = []
        points2 = []
        length = 50
        length2 = 50
        count = 0
        tempcount = 0
        tempcount2 = 0
        foodEaten = 0
        foodEaten2 = 0
        foodJustEaten = False
        foodJustEaten2 = False
        rateOfRemoval = 15
        rateOfRemoval2 = 15
        lengthReached = False
        lengthReached2 = False
        death = False
        death2 = False
        gotPos = False
        food1_eaten = False
        food2_eaten = False
        #highscore = 0
        events = []
        myfont = pygame.font.SysFont("monospace", 15)
        bigFont = pygame.font.SysFont("monospace", 36)
        while 1:
            if pos != 0 and not gotPos:
                food = Food(screen, food1[0], food1[1], food1[2])
                food2 = Food(screen, food2_[0], food2_[1], food2_[2])
                if pos == 1:
                    x = 280
                    x2 = 360
                else:
                    x = 360
                    x2 = 280
                gotPos = True
            events = pygame.event.get()
            if death:
                screen.fill(BLACK)
                deathLabel = bigFont.render("You lose!", 1, (255, 255, 255))
                screen.blit(deathLabel, (width / 2 - 40, height / 2 - 40))
            elif death2:
                screen.fill(BLACK)
                deathLabel = bigFont.render("You win!", 1, (255, 255, 255))
                screen.blit(deathLabel, (width / 2 - 40, height / 2 - 40))
            elif not ready:
                screen.fill(BLACK)
                deathLabel = bigFont.render("Waiting", 1, (255, 255, 255))
                screen.blit(deathLabel, (width / 2 - 40, height / 2 - 40))
            else:
                if len(points) >= length and not lengthReached:
                    lengthReached = True
                if lengthReached and len(points) <= 5 and not death:
                    death = True
                    c.Send({"action":"death"})
                if len(points) >= length2 and not lengthReached2:
                    lengthReached2 = True
                if lengthReached2 and len(points2) <= 5:
                    death2 = True
                #    highscore = count - 720
                tempscore = 0 if count < 720 else count - 720
                label = myfont.render("(" + str(x) + ", " + str(y) + ")" + "        Score: " + str(tempscore), 1, (255, 255, 255))
                foodLabel = myfont.render(str(len(points)) + ", " + str(count) + " " + str(foodEaten) + ", " + str(len(points)) + ", " + str(rateOfRemoval), 1, (255, 255, 255))
                screen.fill(BLACK)
                screen.blit(label, (250, 10))
                screen.blit(foodLabel, (50, 10))
                if which != 0 and new != 0:
                    if which == 1:
                        food = Food(screen, new[0], new[1], new[2])
                        food.draw()
                        print food.x,
                        print food.y
                        tempcount2 = length2
                        length2 += 80
                        foodEaten2 += 1
                        foodJustEaten2 = True
                    else:
                        food2 = Food(screen, new[0], new[1], new[2])
                        food2.draw()
                        print food2.x,
                        print food2.y
                        tempcount2 = length2
                        length2 += 80
                        foodEaten2 += 1
                        foodJustEaten2 = True
                    which = 0
                    new = 0
                
                if food1_eaten:
                    tempcount = length
                    length += 80
                    foodEaten += 1
                    foodJustEaten = True
                    food1_eaten = False
                if food2_eaten:
                    tempcount = length
                    length += 80
                    foodEaten += 1
                    foodJustEaten = True
                    food2_eaten = False
                if tempcount <= length:
                    tempcount += 1
                elif foodEaten > 5 and foodJustEaten:
                    if foodEaten % 2 == 0:
                        if rateOfRemoval > 6:
                            rateOfRemoval -= 1
                            foodJustEaten = False
                if tempcount2 <= length2:
                    tempcount2 += 1
                elif foodEaten2 > 5 and foodJustEaten2:
                    if foodEaten2 % 2 == 0:
                        if rateOfRemoval2 > 6:
                            rateOfRemoval2 -= 1
                            foodJustEaten2 = False
                food.draw()
                food2.draw()
                count += 1
                if count % rateOfRemoval == 0 and lengthReached and len(points) > 0:
                    del points[0]
                    length -= 2
                if count % rateOfRemoval2 == 0 and lengthReached2 and len(points2) > 0:
                    del points2[0]
                    length2 -= 2
                x += dir_x
                y += dir_y
                x2 += dir_x2
                y2 += dir_y2
                points.append((x, y))
                points2.append((x2, y2))
                if len(points) > length:
                    for i in range(0, 1):
                        del points[i]
                if len(points2) > length2:
                    for i in range(0, 1):
                        del points2[i]
                    # del points[0]
                if x <= 0:
                    x = width
                elif x >= width:
                    x = 0
                elif y <= 0:
                    y = height
                elif y >= height:
                    y = 0
                if x2 <= 0:
                    x2 = width
                elif x2 >= width:
                    x2 = 0
                elif y2 <= 0:
                    y2 = height
                elif y2 >= height:
                    y2 = 0
                color = getRand()
                color2 = getRand()
                for point in points:
                    screen.set_at(point, color)
                for point2 in points2:
                    screen.set_at(point2, color)
                screen.set_at((x, y), color)
                screen.set_at((x2, y2), color2)
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            if dir_y == 1:
                                break
                            dir_x = 0
                            dir_y = -1
                        elif event.key == pygame.K_s:
                            if dir_y == -1:
                                break
                            dir_x = 0
                            dir_y = 1
                        elif event.key == pygame.K_a:
                            if dir_x == 1:
                                break
                            dir_x = -1
                            dir_y = 0
                        elif event.key == pygame.K_d:
                            if dir_x == -1:
                                break
                            dir_x = 1
                            dir_y = 0
                        elif event.key == pygame.K_q:
                            if dir_x == 1 and dir_y == 1:
                                break
                            dir_x = -1
                            dir_y = -1
                        elif event.key == pygame.K_e:
                            if dir_x == -1 and dir_y == 1:
                                break
                            dir_x = 1
                            dir_y = -1
                        elif event.key == pygame.K_z:
                            if dir_x == 1 and dir_y == -1:
                                break
                            dir_x = -1
                            dir_y = 1
                        elif event.key == pygame.K_c:
                            if dir_x == -1 and dir_y == -1:
                                break
                            dir_x = 1
                            dir_y = 1
                    c.Send({"action":"loc","loc":(x, y), "dir":(dir_x, dir_y)})
                if food.didHit((x, y)):
                    food1_eaten = True
                    food = Food(screen, random.randint(50, screen.get_width()-50), random.randint(50, screen.get_height()-50), random.randint(10,21))
                    food.draw()
                    print "-",
                    print food.x,
                    print food.y
                    c.Send({'action':'food', 'which':1, 'new':(food.x, food.y, food.foodheight)})
                if food2.didHit((x, y)):
                    food2_eaten = True
                    food2 = Food(screen, random.randint(50, screen.get_width()-50), random.randint(50, screen.get_height()-50), random.randint(10,21))
                    food2.draw()
                    print "-",
                    print food2.x,
                    print food2.y
                    c.Send({'action':'food', 'which':2, 'new':(food2.x, food2.y, food2.foodheight)})
            for event in events:
                if event.type == pygame.QUIT:
                    return
            pygame.display.flip()
            clock.tick(150)
    do()
connect()
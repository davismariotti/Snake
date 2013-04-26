import pygame,random,threading
pygame.init()
global dir_x,dir_y
width = 640
height = 400
x = width/2
y = height/2
dir_x = 0
dir_y = -1
screen = pygame.display.set_mode((640,400))
BLACK = (0,0,0)
clock = pygame.time.Clock()

class Food:
    def __init__(self, s):
        self.foodheight = random.randint(10,21)
        self.screen = screen
        self.x = random.randint(50, screen.get_width()-50)
        self.y = random.randint(50, screen.get_height()-50)
        self.eaten = False
    def draw(self):
        pygame.draw.rect(self.screen, (0,255,0), (self.x, self.y, self.foodheight, self.foodheight))
    def setEaten(self, eaten):
        self.eaten = eaten
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
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
def do(x,y,dir_x,dir_y):
    food = Food(screen)
    points = []
    length = 50
    count = 0
    tempcount = 0
    foodEaten = 0
    foodJustEaten = False
    rateOfRemoval = 15
    lengthReached = False
    death = False
    highscore = 0
    events = []
    myfont = pygame.font.SysFont("monospace", 15)
    bigFont = pygame.font.SysFont("monospace",36)
    while 1:
        events = pygame.event.get()
        if death:
            screen.fill(BLACK)
            deathLabel = bigFont.render("DEATH", 1, (255,255,255))
            highscoreLabel = myfont.render("HighScore: " + str(highscore), 1, (255,255,255))
            screen.blit(deathLabel, (width/2-40,height/2-40))
            screen.blit(highscoreLabel, (width/2-40,height/2+20))
        else:
            if len(points) >= length and not lengthReached:
                lengthReached = True
            if lengthReached and len(points) <= 2:
                death = True
                highscore = count - 720
            tempscore = 0 if count < 720 else count-720
            label = myfont.render("(" + str(x) + ", " + str(y) + ")" + "        Score: " + str(tempscore), 1, (255, 255, 255))
            foodLabel = myfont.render(str(len(points))+", "+str(count)+" "+str(foodEaten) + ", " + str(len(points)) + ", " + str(rateOfRemoval), 1, (255,255,255))
            screen.fill(BLACK)
            screen.blit(label, (250, 10))
            screen.blit(foodLabel, (50, 10))
            if food.isEaten():
                food = Food(screen)
                tempcount = length
                length+=80
                foodEaten+=1
                foodJustEaten = True
            if tempcount <= length:
                tempcount += 1
            elif foodEaten > 5 and foodJustEaten:
                if foodEaten % 2 == 0:
                    if rateOfRemoval > 8:
                        rateOfRemoval-=1
                        foodJustEaten = False
            food.draw()
            count+=1
            if count % rateOfRemoval == 0 and lengthReached:
                del points[0]
                length-=2
            x += dir_x
            y += dir_y
            points.append((x,y))
            if len(points) > length:
                for i in range(0,1):
                    del points[i]
                #del points[0]
            if x <= 0:
                x = width
            elif x >= width:
                x = 0
            elif y <= 0:
                y  = height
            elif y >= height:
                y = 0
            color = getRand()
            for point in points:
                screen.set_at(point, color)
            screen.set_at((x,y),color)
            #AI below
            """def changeDir(dir_x,dir_y):
                rand = random.randint(0,4)
                if rand == 0:
                    if dir_y != 1:
                        return [0,-1]
                    else:
                        changeDir(dir_x,dir_y)
                elif rand == 1:
                    if dir_y != -1:
                        return [0,1]
                    else:
                        changeDir(dir_x,dir_y)
                elif rand == 2:
                    if dir_x != 1:
                        return [-1,0]
                    else:
                        changeDir(dir_x,dir_y)
                elif rand == 3:
                    if dir_x != -1:
                        return [1,0]
                    else:
                        changeDir(dir_x,dir_y)
                else:
                    return [1,1]
            if count%100==0:
                var = changeDir(dir_x,dir_y)
                dir_x = var[0]
                dir_y = var[1]"""
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
            if food.didHit((x,y)):
                food.setEaten(True)
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and death:
                do(x,y,dir_x,dir_y)
                return 
        pygame.display.flip()
        clock.tick(150)
try:
    t = threading.Thread(target=do(x,y,dir_x,dir_y))
    t.start()
    t.join()
except:
    print "bad"
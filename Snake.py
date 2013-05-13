import pygame,random,urllib2
pygame.init()
global dir_x,dir_y
width = 640
height = 400
# Starting locations
x = width/2
y = height/2
dir_x = 0
dir_y = -1
screen = pygame.display.set_mode((640,400))
BLACK = (0,0,0)
clock = pygame.time.Clock()

# A class for food. Initialized everytime a food is eaten
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
        # Checks whether the point is within the food's rect
        if point[0] < self.x or point[0] > self.x + self.foodheight:
            return False
        elif point[1] < self.y or point[1] > self.y + self.foodheight:
            return False
        else:
            return True
def getRand():
    # Used for return a color for the snake
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
def do(x,y,dir_x,dir_y):
    # ----
    # Download the song file from the internet
    f = open("tetris.mid", "wb")
    f.write(urllib2.urlopen("http://gomeow.info/files/tetrisb.mid").read())
    f.close()
    pygame.mixer.init()
    pygame.mixer.music.load("tetris.mid")
    pygame.mixer.music.play(-1)
    # ----
    food = Food(screen) # Initialize the first food
    points = [] # A variable for all the points in the snake
    # A variable for the length of the snake. When this changes, the code will adjust the snake's actual length
    length = 50
    count = 0 # A variable for the count, incremented every loop. Used for score and length changing.
    tempcount = 0
    foodEaten = 0
    foodJustEaten = False
    rateOfRemoval = 15 # A variable for how many loops between each point removal of the back of the snake
    lengthReached = False
    death = False
    highscore = 0
    events = [] # Holds the events of each round, as they are processed in 2 places.
    myfont = pygame.font.SysFont("monospace", 15)
    bigFont = pygame.font.SysFont("monospace",36)
    while 1:
        events = pygame.event.get()
        if death:
            # If you are dead, show the death screen
            screen.fill(BLACK)
            deathLabel = bigFont.render("DEATH", 1, (255,255,255))
            highscoreLabel = myfont.render("HighScore: " + str(highscore), 1, (255,255,255))
            screen.blit(deathLabel, (width/2-40,height/2-40))
            screen.blit(highscoreLabel, (width/2-40,height/2+20))
        else:
            # The code will wait until the full length is reached before starting to remove points.
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
            # Make a new food if it was eaten.
            if food.isEaten():
                food = Food(screen)
                tempcount = length
                length+=80
                foodEaten+=1
                foodJustEaten = True
            if tempcount <= length:
                tempcount += 1
            # If they ate 5 food and they just ate a food
            elif foodEaten > 5 and foodJustEaten:
                if foodEaten % 2 == 0:
                    if rateOfRemoval > 8:
                        rateOfRemoval-=1
                        foodJustEaten = False
            food.draw()
            count+=1
            # Only start removing points after they reach the initial length
            if count % rateOfRemoval == 0 and lengthReached:
                del points[0]
                length-=2
            # Set the e and y to the next point in the direction
            x += dir_x
            y += dir_y
            # Add the points to the list to be drawn later
            points.append((x,y))
            if len(points) > length:
                for i in range(0,1):
                    del points[i]
                #del points[0]
            # The code below allows the snake to wrap around the screen
            if x <= 0:
                x = width
            elif x >= width:
                x = 0
            elif y <= 0:
                y  = height
            elif y >= height:
                y = 0
            # Make the snake a random color
            color = getRand()
            for point in points:
                screen.set_at(point, color)
            for event in events:
                # Change directions
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
            # Set the food as eaten if the snake's head is within the food rect
            if food.didHit((x,y)):
                food.setEaten(True)
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and death:
                do(x,y,dir_x,dir_y)
                return 
        pygame.display.flip()
        clock.tick(150)
# Start
do(x,y,dir_x,dir_y)
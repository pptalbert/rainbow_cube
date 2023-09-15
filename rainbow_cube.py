import pygame
import random
from pygame import mixer
pygame.init()

# CREATING CANVAS
screen_width=500
print("How to play: wasd to move and remember this. Don't touch the border")
canvas = pygame.display.set_mode((screen_width, screen_width))
# TITLE OF CANVAS
pygame.display.set_caption("Rainbow cube")

# play background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# set snake size
left = 0
top = 10
length = 20
width = 20
snake_step=10

#colorcode
colorR=0
colorG=0
colorB=0
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
yellow = (255,255,102)
red = (255,0,0)

# store score
score=0
# exit status
exit = False

# generate rock
rockx = round(random.randrange(0,(screen_width-width))/10.0)*10.0
rocky = round(random.randrange(0,(screen_width-width))/10.0)*10.0
rock_width = width*2
rock_length = length*2
rock_location = [rockx, rocky, rock_width, rock_length]

# snake_list is to store the postition and the color of the snake.
snake_list = []

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift",50)
score_style = pygame.font.SysFont("comicsansms", 35)

# find right food position
def locate_food(rock_location):
    # food_found is a local varable
    food_found = False
    while(not food_found):
        foodx = round(random.randrange(0, (screen_width - width)) / 10.0) * 10.0
        foody = round(random.randrange(0, (screen_width - width)) / 10.0) * 10.0
        if (foodx>=rock_location[0] and foodx<=rock_location[0] + rock_location[2]) and  (foody>=rock_location[1] and foodx<=rock_location[1] + rock_location[3]):
            print("oops, food is in the rock. Relocate it. ")
            continue
        else:
            food_found = True
    return (foodx, foody)

def hit_rock(rock_location, snake_left, snake_top):
        rock_left = rock_location[0]
        rock_top = rock_location[1]
        rock_right = rock_left + rock_location[2]
        rock_bottom = rock_top + rock_location[3]
        if (snake_left>=rock_left and snake_left<=rock_right) and  (snake_top>=rock_top and snake_top<=rock_bottom):
            return True
        else:
            return False

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(canvas, x[2],[x[0], x[1], snake_block, snake_block])
def your_score(score):
    value = score_style.render("Your score: " + str(score), True, yellow)
    canvas.blit(value, [0,0])
def message(msg,color):
    mesg =font_style.render(msg, True,color)
    canvas.blit(mesg, [200,500])

# initialize food
foodx, foody = locate_food(rock_location)
fooda, foodb = locate_food(rock_location)

# entrance

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        # refresh the canvas
        canvas.fill((0, 0, 0))
        snake_block = (left, top, width, length)
        pressed = pygame.key.get_pressed()
        # Hit boundary
        if left > (screen_width-width) or left <0 or top > (screen_width-width) or top < 0:
            message("You lost. Thanks for playing Rainbow Cube",(100,100,100))
            pygame.display.update()
            Death_sound = mixer.Sound('explosion.wav')
            Death_sound.play()
            left = 0
            top = 0
            score=0
            # reset snake
            snake_head = []
            snake_head.append(0)
            snake_head.append(0)
            snake_head.append((colorR, colorG, colorB))
            snake_list = [snake_head]
        #color change
        colorG += 5
        colorR += 3
        colorB += 4
        # check key press
        if pressed[pygame.K_w]:
            top -= snake_step
        if pressed[pygame.K_s]:
            top += snake_step
        if pressed[pygame.K_a]:
            left -= snake_step
        if pressed[pygame.K_d]:
            left +=snake_step
        # check color range
        if colorG > 255:
            colorG = 0
        if colorG <0:
            colorG=255
        if colorR > 255:
            colorR = 0
        if colorR < 0:
            colorR = 255
        if colorB > 255:
            colorB = 100
        if colorB < 0:
            colorB = 255
        # draw food
        pygame.draw.rect(canvas,blue, [foodx, foody, width/2, length/2])
        pygame.draw.rect(canvas,white, [fooda, foodb, width/2, length/2])
        # draw rock
        pygame.draw.rect(canvas,red, [rockx, rocky, rock_width , rock_length])
        # put the current snake block in the list
        snake_head=[]
        snake_head.append(left)
        snake_head.append(top)
        snake_head.append((colorR,colorG,colorB))
        snake_list.append(snake_head)
        if len(snake_list)>(score+1):
            del snake_list[0]
        our_snake(width,snake_list)
        your_score(score)
        pygame.display.update()
        # check whether we hit the rock
        if hit_rock(rock_location,left,top):
            message("aaaahhh",red)
            left=0
            top=0
            score=0
            # reset snake
            snake_head = []
            snake_head.append(0)
            snake_head.append(0)
            snake_head.append((colorR, colorG, colorB))
            snake_list = [snake_head]
            pygame.display.update()
            Death_sound=mixer.Sound('explosion.wav')
            Death_sound.play()
            break
        # check whether we ate the food
        if (foodx>=left and foodx<=(left+width)) and (foody>=top and foody<=(top+width)):
            print("yummy!!")
            foodx, foody = locate_food(rock_location)
            score +=1
            food_sound=mixer.Sound('laser.wav')
            food_sound.play()
        if (fooda>=left and fooda<=(left+width)) and (foodb>=top and foodb<=(top+width)):
            print("yummy!!")
            fooda, foodb = locate_food(rock_location)
            score += 1
            food_sound=mixer.Sound('laser.wav')
            food_sound.play()
        clock.tick(30)

pygame.quit()
quit()


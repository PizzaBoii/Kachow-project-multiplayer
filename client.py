import pygame
import pygame.freetype
import time
import math
import socket
import select
message = ""
client_list = []

pygame.init()

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('127.0.0.1', 5353))



###########################
#keyboard settings
# arrows to change the diplayed settings
# wasd to move
# r to switch between settings
# [ ] to change angles
#[ positive
# ] negative
###############################



# constants
path = ''# you need to have this picture on your pc 3.png'
display_width = 1000
display_height = 1000

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False

#functions

def send(msg, dst_socket):
    dst_socket.send(msg.encode("UTF-8"))


def leave(dst_socket):
    msg = f"{time} {name} Has left the chat!"
    dst_socket.send(msg.encode("UTF-8"))


def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_object(text,font,color):
    textSurface = font.render(text,True,color)
    return (textSurface,textSurface.get_rect())



def message_display(message,cords,color=(0,0,0)):


    large_text=pygame.font.Font('freesansbold.ttf',50)
    Textsurf,TextRect=text_object(message,large_text,color)
    TextRect.center=(cords)
    gameDisplay.blit(Textsurf,TextRect)



def inrange(enemy_pos):
    for i in range(-30,30):
        position = int(enemy_pos[0])+i
        position=str(position)
        if position in enemy_pos[1]:
            return True

    return False

x = (display_width * 0.45)
y = (display_height * 0.8)
x_change = 1

windspeed=0
angle=0


car_speed = 0
side_x=' '
vs=1 #ACCELERATE

# BEGGINING OF THE ACTUAL CODE
enemy_pos = (0, 0)

# print ("initiation program sequence")

enemy_x = -1
enemy_y = -1

while not crashed:
    old_pos_y= enemy_y
    #MORE SETUP SHIT
    gameDisplay.fill(white)
    rlist, wlist, xlist = select.select([my_socket], [my_socket], [])
    for server in rlist:

        enemy_pos= server.recv(1024).decode("UTF-8")
        enemy_pos = enemy_pos.split(',')
        # print (f"before change: {enemy_pos}")


        devide=1
        tof = inrange(enemy_pos)

        if tof and len(enemy_pos)>2:
                devide  = 10**len(enemy_pos[0])


        enemy_x= int(enemy_pos[0])
        enemy_y = int(int(enemy_pos[1])/devide)
        if len(str(enemy_y))>5:
            enemy_y=old_pos_y

        # print (f"after change : {enemy_x} and {enemy_y} {tof} and {devide}")
    if enemy_y>80045:
        asyncio.wait(5)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        ############################
        # MOVE FOR THE CURRENT CLIENT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                side_x='left'
                path =''# you need to have this picture on your pc 2.png' #you will have to have this imagine path on your pc

            elif event.key == pygame.K_d:
                side_x='right'
                path =''# you need to have this picture on your pc 1.png' #you will have to have this imagine path on your pc


            elif event.key==pygame.K_SPACE:
                path = ''# you need to have this picture on your pc 3.png' #you will have to have this imagine path on your pc
                side_x = " "

        ######################





    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        y -= 8
    if pressed[pygame.K_s]:
        y += 8
    if pressed[pygame.K_LEFTBRACKET]:
        angle=angle+1
    if pressed[pygame.K_RIGHTBRACKET]:
        angle=angle-1

    if side_x=='left': #x_change>-15
        x_change-=vs

    if side_x=='right':#and x_change<15
       x_change+=vs

    if side_x==" ":
        x_change=x_change*0.9


    x += x_change
    ##
    carImg = pygame.image.load(path)

    car(x, y)
    if enemy_y!=-1 and enemy_x!=-1:
        car(enemy_x, enemy_y)
        message_display(f"p2", (enemy_x + 20, enemy_y-30))

    if x>display_width:
        x=0
    if x<0:
        x=display_width-50


    if y<0:
        y= display_height-50
    if y>display_height:
        y=5


    message_display(f"({int(x)},{int(y)})- speed of the car:{int(x_change)}", (500, 24))
    send(f"{int(x)},{int(y)}", my_socket)
    message_display(f"p1", (x + 20, y - 30))

    message_display(f"speed rate -  {vs}", (1500, 24))

    # if -5<x_change<5 and path==''# you need to have this picture on your pc 3.png' and vs!=0:
        # message_display("KACHOW",(x,y-30),(255,0,0))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()

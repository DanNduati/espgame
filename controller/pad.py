import pygame
import socket

class display:
    def __init__(self):
        self.x = 10
        self.y = 10
    def printText(self,screen,string):
        font=pygame.font.Font(None,20)
        text=font.render(string,True,BLACK)
        screen.blit(text,[self.x,self.y])
        #indent 
        self.y+=12

#udp
UDP_IP_ADDRESS = "192.168.8.101"
UDP_PORT_NO = 6969
bufferSize = 1024
#canvas
BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.init()
size = [500,200]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dualshock 3')
done = False
#screen update clock
clock = pygame.time.Clock()
pygame.joystick.init()
clientSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def sendPacket(data):
    clientSock.sendto(data.encode('utf-8'),(UDP_IP_ADDRESS,UDP_PORT_NO))
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)

    #get game controller counts
    controller_count= pygame.joystick.get_count()
    #create a display object
    disp = display()
    disp.printText(screen,'Controllers connected: {}'.format(controller_count))
    #display(screen,'Controller count: {}'.format(controller_count))
    #connect to the first controller
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        #get controller name
        name = joystick.get_name()
        disp.printText(screen,'Controller name: {}'.format(name))
        #left joystick axis values
        xval = joystick.get_axis(3)
        yval = joystick.get_axis(4)
        startBtn = joystick.get_button(9)
        #apparently to use .format with json one has to escape all json curly
        #braces poof 
        message = """{{"x":{:>6.3f},"y":{:>6.3f},"s":{}}}""".format(xval,yval,startBtn)
        sendPacket(message)
        disp.printText(screen,'left joystick X value: {}'.format(xval))
        disp.printText(screen,'Left joystick Y value: {}'.format(yval))
        disp.printText(screen,'Start button Value: {}'.format(startBtn))
    except:
        print("No controller connected!")
        break
    pygame.display.flip()
    clock.tick(2000000)
pygame.quit()

import socket
import pygame

class Dualshock:
    def __init__(self,id):
        self.loopFlag = True
        pygame.joystick.init()
        self.keyMap = {'joyX':3,'joyY':4,'start':9}
        self.__id = id
        #canvas variables
        self.clock = pygame.time.Clock()
        self.x = 10
        self.y = 10
        self.width = 500
        self.height = 200
        self.size = [self.width,self.height]
        #udp 
        self.UDP_IP_ADDRESS = "192.168.0.182"
        self.UDP_PORT = 6969
        self.bufferSize = 1024

    def init(self):
        #controller intialization
        self.controller = pygame.joystick.Joystick(self.__id)
        self.controller.init()
        #display initialization
        self.screen =pygame.display.set_mode(self.size)
        pygame.display.set_caption('Controller States')
        self.screen.fill((255,255,255))
        #udp init
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def displayInfo(self,screen,string):
        self.font = pygame.font.Font(None,20)
        self.text = self.font.render(string,True,(0,0,0))
        screen.blit(self.text,[self.x,self.y])
        #indent
        self.y+=12

    def getBtn(self,id):
        self.state = self.controller.get_button(id)
        return self.state

    def getAxis(self,id):
        self.value = self.controller.get_axis(id)
        return self.value

    def getControlStates(self):
        pygame.init()
        self.init()
        self.clock = pygame.time.Clock()
        while self.loopFlag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loopFlag = False
            self.screen.fill((255,255,255))
            self.xval = self.getAxis(self.keyMap['joyX'])
            self.yval = self.getAxis(self.keyMap['joyY'])
            self.startBtn = self.getBtn(self.keyMap['start'])
            values = (self.xval,self.yval,self.startBtn)
            self.message = '''x:{},y:{},s:{}'''.format(self.xval,self.yval,self.startBtn)
            self.clientSocket.sendto(self.message.encode('utf-8'),(self.UDP_IP_ADDRESS,self.UDP_PORT))
            #ack
            self.data,self.addr = self.clientSocket.recvfrom(self.bufferSize)
            print("received: ",self.data," from: ",self.addr)
            #display the controller states
            #self.displayInfo(self.screen,'Left joystick x value: {}'.format(self.xval))
            #self.displayInfo(self.screen,'Left joystick y value: {}'.format(self.yval))
            #self.displayInfo(self.screen,'Left joystick x value: {}'.format(self.startBtn))
            #pygame.display.flip()
            self.clock.tick(500)
        self.clientSocket.close()
        pygame.quit()

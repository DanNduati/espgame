import utime
from utime import sleep_ms,ticks_ms,ticks_us,ticks_diff
from machine import Pin,I2C
from random import getrandbits,seed
import ssd1306
import socket
import wifi
import server

class Esp32game():
    def __init__(self):
        self.timer = 0
        seed(ticks_us())
        self.btnRef = 0
        self.btnUval = 0
        self.btnDval = 0
        self.btnLval = 0
        self.btnRval = 0
        self.frameRate = 30
        self.screenWidth = 128
        self.screenHeight = 64
        self.Btns = 0
        self.lastBtns = 0
        #configure oled display i2c
        self.i2c = I2C(scl=Pin(22),sda=Pin(21))
        self.display =ssd1306.SSD1306_I2C(self.screenWidth,self.screenHeight,self.i2c)
        #connect to wifi and create udp server
        wifi.connect()
        server.createSocket()

    def getBtn(self):
        self.data = server.getData()
        xval = self.data[0]
        yval = self.data[1]
        self.btnRef = self.data[2]
        self.btnLval = 1 if xval<-0.5 else 0
        self.btnRval = 1 if xval>0.5 else 0
        self.btnUval = 1 if yval<-0.5 else 0
        self.btnDval = 1 if yval>0.5 else 0
        self.lastBtns = self.Btns
        self.Btns = 0
        self.Btns = self.Btns | self.btnUval << 1 | self.btnLval << 2 | self.btnRval << 3 | self.btnDval << 4 | self.btnRef << 5
        print(self.Btns)
        return self.Btns


    def random(self,x,y):
        return(getrandbits(20)%(y-x+1)+x)

    def dispNwait(self):
        self.display.show()
        timer_dif = int(1000/self.frameRate)-ticks_diff(ticks_ms, self.timer)
        if timer_dif>0:
            sleep_ms(timer_dif)
        self.timer = ticks_ms

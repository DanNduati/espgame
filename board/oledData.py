import machine
import ssd1306
import wifi
import socket
import server
import framebuf
i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64,i2c)

#connect to wifi
wifi.connect()
server.createSocket()

def drawUI():
    #clear the display
    display.fill(0)
    display.rect(0,0,128,64,1)
    display.line(45,0,45,64,1)
    display.line(0,21,128,21,1)
    display.line(0,41,128,41,1)
    display.text('x',20,5)
    display.text('y',20,26)
    display.text('start',5,47)

def displayVals(x,y,s):
    display.text('{}'.format(str(x)),48,5)
    display.text('{}'.format(str(y)),48,26)
    display.text('{}'.format(str(s)),48,47)
    display.show()

def main():
    drawUI()
    try:
        values = server.getData()
    except:
        print("Error trying to get data check network")
    x = values[0]
    y = values[1]
    s = values[2]
    displayVals(x,y,s)
while True:
    main()

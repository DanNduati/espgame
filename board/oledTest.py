import machine
import ssd1306
import framebuf

i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64,i2c)
#clear the screen
#display.fill(0)
#display.text('Barcelona',0,0)
#display.text('Says',0,16)
#display.text('Hello',0,32)
#display.show()
#display bitmap images
with open('barca.pbm','rb') as f:
    f.readline()
    f.readline()
    f.readline()
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data,128,64,framebuf.MONO_HLSB)
display.invert(1)
display.blit(fbuf,0,0)
display.show()

from machine import Pin, SPI
import time

load = Pin(28, Pin.OUT)	#shift register - buttons
cs1 = Pin(5, Pin.OUT)	#shift register - buttons


rx_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

arr_byte = bytearray([0b0010_1000,0b0011_1000,0b0011_0000,0b0000_0101,0b0000_0110])

# Initialize SPI //data=mosi shift=sck
spi1 = SPI(0,
          baudrate=400000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(2),
          mosi=Pin(3),
          miso=(4))



def button_read():
    load.value(0); load.value(1)  # Single-line pulse
    cs1.value(0)
    data = spi1.read(2, 0x00)
    cs1.value(1)
    
    return [(int.from_bytes(data, 'big') >> (15 - i)) & 1 for i in range(16)]


while True:
    time.sleep_ms(100)
    print(button_read())
 
    
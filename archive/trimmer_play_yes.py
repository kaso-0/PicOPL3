from machine import Pin, SPI
import time
import random


# Assign chip select (CS) pin and initialize it high
a0 = Pin(14, Pin.OUT)	#OPL3	14
a1 = Pin(15, Pin.OUT)	#OPL3	15
latch = Pin(17, Pin.OUT)#OPL3	17
reset = Pin(16, Pin.OUT)#OPL3 clear
shift_latch = Pin(22, Pin.OUT)#shift register
load = Pin(28, Pin.OUT)	#shift register - buttons
cs1 = Pin(5, Pin.OUT)	#shift register - buttons
adc1 = machine.ADC(26)    #analog multiplexer - potentiometrs and keys
A2 = Pin(8, Pin.OUT)    #analog multiplexer
B2 = Pin(9, Pin.OUT)    #analog multiplexer
C2 = Pin(10, Pin.OUT)    #analog multiplexer
A3 = Pin(11, Pin.OUT)    #analog multiplexer
B3 = Pin(12, Pin.OUT)    #analog multiplexer
C3 = Pin(13, Pin.OUT)    #analog multiplexer

arr_byte = bytearray([0x50,0x70,0x60,0x05,0x06]) #numero tres jsou "nizsi multiplexer"
arr_analog = [0, 0, 0, 0, 0 ] # analog arry
rx_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] # array for recieving buttons
arr_byte_but = bytearray([0b0010_1000,0b0011_1000,0b0011_0000,0b0000_0101,0b0000_0110]) # array for order of buttons
array2 = [0, 0, 0, 0, 0, 0, 0, 7, 4, 5, 6, 0, 3, 2, 1, 0, ] # array that defines what button should do

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

spi = SPI(0,
    baudrate=400000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(18),
    mosi=Pin(19)) 
reset = Pin(16, Pin.OUT)#must be here because micropython

latch.value(1)
reset.value(1)
a0.value(0)
a1.value(0)
    
def opl_reset():
    reset.value(0)
    time.sleep_ms(1)
    reset.value(1) #clear registers of OPL2.
    time.sleep_ms(1)

def opl2_write(register, low_value): #low_value = value of "lower" register
    a1.value(0)
    a0.value(0)  # Set A0, A1 low to indicate it's a lower register address
    spi.write(bytearray([register]))
    latch.value(0)
    latch.value(1)  # Latch the lower register address
    
    a0.value(1)  # Set A0 high to indicate it's data
    spi.write(bytearray([low_value]))
    latch.value(0)
    latch.value(1)  # Latch the data to lower register

def opl3_write(register, low_value, high_value): #low_value = value of "lower" register
    a1.value(0)
    a0.value(0)  # Set A0, A1 low to indicate it's a lower register address
    spi.write(bytearray([register]))
    latch.value(0)
    latch.value(1)  # Latch the lower register address
        
    a0.value(1)  # Set A0 high to indicate it's data
    spi.write(bytearray([low_value]))
    latch.value(0)
    latch.value(1)  # Latch the data to lower register
    
    a0.value(0)    
    a1.value(1)# Set A0 low and A1 high to indicate it's a higher register address
    spi.write(bytearray([register]))
    latch.value(0)
    latch.value(1)  # Latch the higher register address

    a0.value(1)  # Set A0 high to indicate it's data, A1 dont care
    spi.write(bytearray([high_value]))
    latch.value(0)
    latch.value(1)  # Latch the data to higher register
    a1.value(0)

def opl3_init(frequency, offset): #channel offset, frequency select
    opl3_write(0x05, 0x00, 0x01)  # Set to opl2 mode
    opl3_write(0x20 + offset, 0xa9, 0xa4)  # Set operator 1 frequency multiplier
    opl3_write(0x40 + offset, 0x02, 0x00)  # Set operator 1 level
    opl3_write(0x60 + offset, 0x44, 0x76)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x80 + offset, 0xe5, 0x20)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x23 + offset, 0x07, 0x0f)  # Set the carrier's multiple to 1
    opl3_write(0xa0 + offset, 0x00 + frequency, 0x00 + frequency)  # Set frequency number
    opl3_write(0x43 + offset, 0x04, 0x04)  # Set the carrier to maximum volume (about 47 dB)
    #opl3_write(0x63 + offset, 0x30, 0x30)  # Carrier attack:  quick;   decay:   long
    #opl3_write(0x83 + offset, 0x33, 0x33)  # Carrier sustain: medium;  release: medium
    opl3_write(0xe3 + offset, 0x01, 0x03)  #
    opl3_write(0xb0 + offset, 0x22, 0x22)  # Turn the voice on; set the octave and freq MSB
    opl3_write(0xc0 + offset, 0xf0, 0xf0)  # feedback , algoritmh
    opl3_write(0xbd + offset, 0x00, 0x00)

def analog_read():
    n = len(arr_byte)
    for x in range(n):
        idk = arr_byte[x]
        A2.value(idk & 0b0000_0001)
        B2.value(idk & 0b0000_0010)
        C2.value(idk & 0b0000_0100)
        A3.value(idk & 0b0001_0000)
        B3.value(idk & 0b0010_0000)
        C3.value(idk & 0b0100_0000)
        time.sleep_us(1)
        arr_analog[x] = adc1.read_u16()>>8

def button_read():
    load.value(0); load.value(1)  # Single-line pulse
    cs1.value(0)
    data = spi1.read(2, 0x00)
    cs1.value(1)
    return [(int.from_bytes(data, 'big') >> (15 - i)) & 1 for i in range(16)]
triggered = 0

opl_reset()
opl3_init(0, 0)
opl3_init(0, 1)
previous_press = 1
while True:
    analog_read()
    opl3_write(0xa0, arr_analog[0], arr_analog[0])
    opl3_write(0xa0 + 1, arr_analog[1], arr_analog[1])
    opl3_write(0x63, arr_analog[2], arr_analog[2])
    opl3_write(0x63 + 1, arr_analog[3], arr_analog[3])
    for button_number in range(len(button_read())):
        if button_read()[button_number] == 0:  # Check if the button is pressed and play diffrent waveform depending on array2
            opl3_write(0xe3, 0x00, 0x00 + array2[button_number])
            opl3_write(0xe3 + 1, 0x00, 0x00 + array2[button_number])
    if button_read()[6] == 0 and previous_press == 1 and not triggered : #button for opl reset
        print("kaso")
        opl_reset()
        opl3_init(0, 0)
        opl3_init(0, 1)
        triggered = 1
    if button_read()[6] == 1 and previous_press == 0: triggered = 0 #debounce for opl reset button
    #print(button_read())
    time.sleep_ms(5)
    previous_press = button_read()[6]
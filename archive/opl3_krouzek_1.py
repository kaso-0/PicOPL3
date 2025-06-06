from machine import Pin, SPI
import time
import random

    # Assign chip select (CS) pin and initialize it high
a0 = Pin(14, Pin.OUT)	#OPL3	14
a1 = Pin(15, Pin.OUT)	#OPL3	15
latch = Pin(17, Pin.OUT)#OPL3	17
reset = Pin(16, Pin.OUT)#OPL3 clear
shift_latch = Pin(22, Pin.OUT)#shift register
print("opl 3")

    # Initialize SPI //data=mosi shift=sck
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
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the lower register address
        
    a0.value(1)  # Set A0 high to indicate it's data
    spi.write(bytearray([low_value]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the data to lower register

def opl4_write(register, low_value): #low_value = value of "lower" register
    a1.value(0)
    a0.value(1)  # Set A0, A1 low to indicate it's a lower register address
    spi.write(bytearray([register]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the lower register address
        
    a1.value(1)  # Set A0 high to indicate it's data
    spi.write(bytearray([low_value]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the data to lower register

def opl3_write(register, low_value, high_value): #low_value = value of "lower" register
    a1.value(0)
    a0.value(0)  # Set A0, A1 low to indicate it's a lower register address
    spi.write(bytearray([register]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the lower register address
        
    a0.value(1)  # Set A0 high to indicate it's data
    spi.write(bytearray([low_value]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the data to lower register
    
    a0.value(0)    
    a1.value(1)# Set A0 low and A1 high to indicate it's a higher register address
    spi.write(bytearray([register]))
    latch.value(0)
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the higher register address

    a0.value(1)  # Set A0 high to indicate it's data, A1 dont care
    spi.write(bytearray([high_value]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    latch.value(1)  # Latch the data to higher register
    
    a1.value(0)
    
def opl3_init(frequency): #channel offset, frequency select
    opl3_write(0x05, 0x00, 0x01)  # Set to opl2 mode
    opl3_write(0x20, 0xa9, 0xa4)  # Set operator 1 frequency multiplier
    opl3_write(0x40, 0x02, 0x00)  # Set operator 1 level
    opl3_write(0x60, 0x44, 0x76)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x80, 0xe5, 0x20)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x23, 0x07, 0x0f)  # Set the carrier's multiple to 1
    opl3_write(0xa0, 0x00 + frequency, 0x00 + frequency)  # Set frequency number
    opl3_write(0x43, 0x04, 0x04)  # Set the carrier to maximum volume (about 47 dB)
    opl3_write(0x63, 0x30, 0x30)  # Carrier attack:  quick;   decay:   long
    opl3_write(0x83, 0x33, 0x33)  # Carrier sustain: medium;  release: medium
    #opl3_write(0xe3, 0x01, 0x01)  #
    #opl3_write(0xe0, 0x00, 0x01)  # 
    opl3_write(0xb0, 0x22, 0x22)  # Turn the voice on; set the octave and freq MSB
    opl3_write(0xc0, 0xf0, 0xf0)  # feedback , algoritmh
    opl3_write(0xbd, 0x00, 0x00)
    #time.sleep(1)
    #opl2_write(0xb0 + offset, 0x01)  # Turn the voice off; set the octave and freq MSB
    #time.sleep(0.2)

#opl2_init(1, 50)
opl_reset()
opl3_init(200)  # Turn the voice on; set the octave and freq MSB

x = 0
while True:
    if x == 255:
        x = 0
    opl3_init(x)
    x = x +1
    print(x)










while 1 == 0 :
    time.sleep(0.2)    
    opl4_write(0x2A, 0xa5)# Tremolo Vibrato
    opl4_write(0x2D, 0x86)
    opl4_write(0x2A, 0)#Key scale
    opl4_write(0x2D, 0)
    opl4_write(0x2A, 0)# attact
    opl4_write(0x2D, 0)
    opl4_write(0x2A, 0)#sustain
    opl4_write(0x2D, 0)
    opl4_write(0xa5, 245)
    x += 1
    print(x)

from machine import Pin, SPI
import time

# Assign chip select (CS) pin and initialize it high
a0 = Pin(14, Pin.OUT)	#OPL3	14
a1 = Pin(15, Pin.OUT)	#OPL3	15
latch = Pin(17, Pin.OUT)#OPL3	17
reset = Pin(16, Pin.OUT)#OPL3 clear
shift_latch = Pin(22, Pin.OUT)#shift register

   

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
    
def opl3_reset():
    reset.value(0)
    time.sleep_ms(1)
    reset.value(1) #clear registers of OPL2.
    time.sleep_ms(1)
    
    
def opl3_write(register, value):
    a1.value(1)
    a0.value(0)  # Set A0 low to indicate it's a register address
    time.sleep_us(100)
    spi.write(bytearray([register]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    time.sleep_us(100)
    latch.value(1)  # Latch the register address
    
    time.sleep_us(100)
    
    a0.value(1)  # Set A0 high to indicate it's data
    time.sleep_us(100)
    spi.write(bytearray([value]))
    latch.value(0)
    
    shift_latch.value(1)
    shift_latch.value(0)
    time.sleep_us(100)
    latch.value(1)  # Latch the data
    
    time.sleep_us(100)
    a1.value(0)
    
def opl3_init(offset, frequency): #channel offset, frequency select
    opl3_reset()

    opl3_write(0x20 + offset, 0xa9)  # Set operator 1 frequency multiplier
    opl3_write(0x40 + offset, 0x0c)  # Set operator 1 level
    opl3_write(0x60 + offset, 0x74)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x80 + offset, 0xf5)  # Set operator 1 amplitude envelope parameters
    opl3_write(0x23 + offset, 0x03)  # Set the carrier's multiple to 1
    opl3_write(0xa0 + offset, 0x98 + frequency)  # Set frequency number
    opl3_write(0x43 + offset, 0x04)  # Set the carrier to maximum volume (about 47 dB)
    opl3_write(0x63 + offset, 0xf0)  # Carrier attack:  quick;   decay:   long
    opl3_write(0x83 + offset, 0x00)  # Carrier sustain: medium;  release: medium
    opl3_write(0xe3 + offset, 0x01)  #
    opl3_write(0xe0 + offset, 0x03)  # 
    opl3_write(0xb0 + offset, 0x22)  # Turn the voice on; set the octave and freq MSB
    opl3_write(0xc0 + offset, 0x00)  # feedback , algoritmh
    opl3_write(0xbd + offset, 0x00)
    #time.sleep(1)
    #opl3_write(0xb0 + offset, 0x01)  # Turn the voice off; set the octave and freq MSB
    #time.sleep(0.2)


opl3_init(1, 50)
opl3_write(0xb0, 0x01)

opl3_write(0xb0, 0x22)
#opl3_write(random.getrandbits(8), random.getrandbits(8))


opl3_write(152, 5) #dulezite
opl3_write(31, 200) #dulezite


#musi byt jeden radek, jinak nehraje
opl3_write(254, 100) #meni ton kdyz neni
opl3_write(207, 215) #meni ton kdyz neni

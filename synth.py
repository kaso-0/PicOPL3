from machine import Pin, SPI
import machine
import time
import random
# Assign chip select (CS) pin and initialize it high
a0 = Pin(14, Pin.OUT)	#OPL3	14
a1 = Pin(15, Pin.OUT)	#OPL3	15
latch = Pin(17, Pin.OUT)#OPL3	17
reset = Pin(16, Pin.OUT)#OPL3 initiel clear
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

#arr_byte_but = bytearray([0b0010_1000,0b0011_1000,0b0011_0000,0b0000_0101,0b0000_0110]) neco nevic, netusim
#print("opl 3")

    # Initialize SPI //data=mosi shift=sck
spi1 = SPI(0,		#for button read
          baudrate=400000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(2),
          mosi=Pin(3),
          miso=(4))

spi = SPI(0,	#for OPL3
        baudrate=400000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(18),
        mosi=Pin(19))

reset = Pin(16, Pin.OUT) #must be here because micropython, OPL3 reset pin

arr_byte = bytearray([0x50,0x70,0x60,0x05,0x06,0x40,0x10,0x20,0x07,0x04,   0x34,0x36,0x37,0x35,0x33,0x30,0x31,0x32,0x03,0x02,0x01,0x00]) #dolni cislice jsou "nizsi multiplexer" - takze nejdriv napsat adresu vyssiho multiplexeru, pak nizsi. nejdriv cteni potenciometru, pak keys
arr_analog_pot = [0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0]		#contains analog values of 10 potentiometers located on board "left to right, up to down"
arr_analog_key = [0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 0, 0]	#contains analog values of 12 keys located on board "left to right"
rx_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #contains bool values of 16 buttons located on board "top right corner"

class opl:
    def reset():
        reset.value(0)
        time.sleep_ms(1)
        reset.value(1) #clear registers of OPL2.
        time.sleep_ms(1)


    def write(register, low_value, high_value): #low_value = value of "lower" register
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

    def init(frequency, offset): #channel offset, frequency select
        latch.value(1)
        reset.value(1)
        a0.value(0)
        a1.value(0)
    
        time.sleep_ms(10)
    
        opl.write(0x05, 0x00, 0x01)  # Set to opl2 mode
        opl.write(0x20 + offset, 0xa9, 0xa4)  # Set operator 1 frequency multiplier
        opl.write(0x40 + offset, 0x02, 0x00)  # Set operator 1 level
        opl.write(0x60 + offset, 0x44, 0x76)  # Set operator 1 amplitude envelope parameters
        opl.write(0x80 + offset, 0xe5, 0x20)  # Set operator 1 amplitude envelope parameters
        opl.write(0x23 + offset, 0x07, 0x0f)  # Set the carrier's multiple to 1
        #opl.write(0xa0 + offset, 0x00 + frequency, 0x00 + frequency)  # Set frequency number
        opl.write(0x43 + offset, 0x04, 0x04)  # Set the carrier to maximum volume (about 47 dB)
        opl.write(0x63 + offset, 0x30, 0x30)  # Carrier attack:  quick;   decay:   long
        opl.write(0x83 + offset, 0x33, 0x33)  # Carrier sustain: medium;  release: medium
        opl.write(0xe3 + offset, 0x01, 0x03)  #
        #opl.write(0xe0, 0x00, 0x01)  # 
        opl.write(0xb0 + offset, 0x22, 0x22)  # Turn the voice on; set the octave and freq MSB
        opl.write(0xc0 + offset, 0xf0, 0xf0)  # feedback , algoritmh
        opl.write(0xbd + offset, 0x00, 0x00)
        #opl.write(0xE0 + offset, 0xc0, 0xc0)
        #time.sleep(0.2)

def analog_read():
    for x in range(10):		#reads potentiometer values
        idk = arr_byte[x]
        A2.value(idk & 0b0000_0001)
        B2.value(idk & 0b0000_0010)
        C2.value(idk & 0b0000_0100)
        A3.value(idk & 0b0001_0000)
        B3.value(idk & 0b0010_0000)
        C3.value(idk & 0b0100_0000)
        time.sleep_us(1)
        arr_analog_pot[x] = adc1.read_u16()>>8
        
    for x in range(12):		#reads keys analog values
        idk = arr_byte[x+10]
        A2.value(idk & 0b0000_0001)
        B2.value(idk & 0b0000_0010)
        C2.value(idk & 0b0000_0100)
        A3.value(idk & 0b0001_0000)
        B3.value(idk & 0b0010_0000)
        C3.value(idk & 0b0100_0000)
        time.sleep_us(1)
        arr_analog_key[x] = adc1.read_u16()>>8
    
def button_read():
    load.value(0); load.value(1)  # Single-line pulse
    cs1.value(0)
    data = spi1.read(2, 0x00)
    cs1.value(1)
    button_mask = [0xfffe, 0xfffd, 0xfffb, 0xfff7, 0xff7f, 0xffbf, 0xffdf, 0xfeff, 0xfdff, 0xfbff, 0xf7ff,0x7fff, 0xbfff, 0xffef, 0xdfff, 0xefff]
    data_int = int.from_bytes(data, 'big')
    for x in range(16):
        rx_buttons[x] = (data_int | button_mask[x])!=0xffff
from machine import Pin, SPI
import time
import random

adc1 = machine.ADC(26)    #analog multiplexer - potentiometrs and keys

A2 = Pin(8, Pin.OUT)    #analog multiplexer
B2 = Pin(9, Pin.OUT)    #analog multiplexer
C2 = Pin(10, Pin.OUT)    #analog multiplexer
A3 = Pin(11, Pin.OUT)    #analog multiplexer
B3 = Pin(12, Pin.OUT)    #analog multiplexer
C3 = Pin(13, Pin.OUT)    #analog multiplexer

arr_byte = bytearray([0x50,0x70,0x60,0x05,0x06]) #numero tres jsou "nizsi multiplexer"

arr_analog = [0, 0, 0, 0, 0 ]


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
        
while True:
    analog_read()    
    print(arr_analog)
    time.sleep_ms(88)
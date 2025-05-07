from machine import Pin, SPI
import machine
import time
import random
import synth

array2 = [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, ] #array for button mapping

synth.opl.reset()
synth.opl.init(0)
synth.opl.init(1)

while True:
    synth.analog_read()
    synth.button_read()
    print(synth.arr_analog_pot)
    print(synth.arr_analog_key)
    print(synth.rx_buttons)
    #print(rx_buttons)
    time.sleep_ms(10)
    synth.opl.write(0xa0, synth.arr_analog_pot[0], synth.arr_analog_pot[0])
    synth.opl.write(0xa0 + 1, synth.arr_analog_pot[1], synth.arr_analog_pot[1])
    for button_number in range(len(synth.rx_buttons)):
        if synth.rx_buttons[button_number] == True:  # Check if the button is pressed
            synth.opl.write(0xe3, 0x00, 0x00 + array2[button_number])
            synth.opl.write(0xe4, 0x00, 0x00 + array2[button_number])
            
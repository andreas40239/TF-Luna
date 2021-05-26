import time
import numpy as np

import tfluna
import timeout_decorator

with tfluna.TfLuna(serial_name = "/dev/ttyUSB0", baud_speed=115200) as tfluna:
    try:
        tfluna.get_version()
        tfluna.set_samp_rate(10)
        #tfluna.set_baudrate(57600)
        #tfluna.set_baudrate(115200)

        for i in range(10):
            distance,strength,temperature = tfluna.read_tfluna_data() # read values
            print(
                f"Distance: {distance:2.2f} m, "
                f"Strength: {strength:2.0f} / 65535 (16-bit), "
                f"Chip Temperature: {temperature:2.1f} C") # print sample data
    
    except timeout_decorator.TimeoutError:
        print(f"Timeout while communicating with the Tf Luna sensor, exiting")
from smbus2 import SMBus 
import time 

i2c_ch = 1
i2c_address = 0x48

reg_config = 0b01
reg_conversion = 0b00

bus = SMBus(i2c_ch)
config = [0b11000010,0b10000011]

while True:
    bus.write_i2c_block_data(i2c_address, reg_config, config)
    time.sleep(0.01)
    result = bus.read_i2c_block_data(i2c_address, reg_conversion, 2)
    value = ((result[0]) << 8 | (result[1]))

    print(bin(value))
    if value & 0x8000 !=0:
        value -= 1 << 16
    v = value * 4096 / 32768
    v = v/1000
    print(f'A0: {v} V')
    time.sleep(1)


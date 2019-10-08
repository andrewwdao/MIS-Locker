import time
import ads1115.ads1115 as ADS
from ads1115.analog_in import AnalogIn


# ---------------------------- Private Parameters:
# -----Address and Screen parameter:
ADS_ADDRESS = 0x48
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(ADS_ADDRESS)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)

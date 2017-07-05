import os
import datetime
import glob
import time
import sys
from beebotte import *


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
output = open('reading.csv','w')

bbt = BBT('b9e4f10ec853c422475f193714a40334', '5303fb9b2077bd3f9db4df8916a73093b84ecee3d8fd2b96db4466de252b9160')
temp_resource   = Resource(bbt, 'RaspberryPi', 'temperature')
hashrate_resource   = Resource(bbt, 'RaspberryPi', 'total_hashrate')
hashrate_calculated_resource   = Resource(bbt, 'RaspberryPi', 'total_hashrate_calculated')

eth_pool_url='http://dwarfpool.com/eth/api?wallet=4010442e78aa9a8eb406436c0fbb23a859d34fbe&email=thesatishk@icloud.com'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_tempc():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def read_tempf():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

while True:
  #print('C =%3.3f F = %3.3f'% read_temp())
  try:
      #output.write(time.strftime("%H:%M:%S")+', '+(time.strftime("%d/%m/%Y"))+',C =%3.3f'% read_tempc())
      temp_resource.write(read_tempc())
      #output.write('\n')
      response = urllib.urlopen(eth_pool_url)
      data = json.loads(response.read())
      hashrate_resource.write(data["total_hashrate"])
      hashrate_calculated_resource.write(data["total_hashrate_calculated"])
      time.sleep(300)
  except KeyboardInterrupt:
      #output.close()
      print("Saving output file")
      sys.exit()

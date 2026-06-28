import serial
import random
import time

SP = serial.Serial()
SP.port = "COM3"
SP.baudrate = 9600

SP.open()

if SP.isOpen :
   # Sart of frame and packet ID
   data = [0x23, random.randint(0, 126)]

   # Frame length
   length = random.randint(1, 128)
   data.append(length)

   # Frame data
   for idx in range(length):
      data.append(random.randint(48,126))

   # Frame checksum
   checksum = 0
   for value in data:
      checksum ^= value
   data.append(checksum)

   # End of Frame
   data.append(0x24)

   SP.write(bytes(data))
   SP.flush()
   time.sleep(1)
   SP.close()
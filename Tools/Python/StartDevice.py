import serial
import time

SP = serial.Serial()
SP.port = "COM3"
SP.baudrate = 9600
SP.parity = serial.PARITY_EVEN
SP.stopbits = 1
SP.open()
SP.timeout = 0.5

def __SendCmd__(cmd):

   cmdSended = False
   answer = []
   SP.write(bytes(cmd))
   SP.reset_input_buffer()

   # Wait ACK
   answer = SP.read(1)

   if answer[0] == 0x79:
      cmdSended = True
      
   return cmdSended

if SP.isOpen :
   # Start bootloader in UART mode
   data = [0x7F]
   SP.write(bytes(data))
   SP.reset_input_buffer()

   # Wait ACK
   answer = []
   answer = SP.read(1)

   if answer.__len__() > 0:
      if answer[0] == 0x79:
         # Send "Go" command
         cmd = [0x21, 0xDE]
         if __SendCmd__(cmd):

            # Address to jump
            adrr = [0x08, 0x00, 0x00, 0x00]

            # Checksum calcul
            checksum = 0x00
            for byte in adrr:
               checksum ^= byte
            adrr.append(checksum)

            __SendCmd__(adrr)

SP.close()
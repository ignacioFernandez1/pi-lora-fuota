from network import LoRa
import socket
import time
import binascii
import pycom

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C, adr=True)

dev_eui = binascii.unhexlify('c5c65c3303799380'.replace(' ', ''))
app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ', ''))
app_key = binascii.unhexlify('80 4d 8b 48 50 98 62 be 9d 84 a7 db ae 7c 4a 88'.replace(' ', ''))
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

print("devEUI {}".format(binascii.hexlify(lora.mac())))

pycom.heartbeat(False)
pycom.rgbled(0x111111)

print(lora.stats().tx_frequency)

while not lora.has_joined():
    time.sleep(1)
    print('.', end='')
print('Network joined!')


print(lora.stats().tx_frequency)

send_interval = 1
seconds = 30
count = 0
while True:
    count += 1
    print("Send data loop %d" % count)
    pycom.heartbeat(False)
    pycom.rgbled(0x32CD32)  # LIMEGREEN LED
    time.sleep(1)
    pycom.rgbled(0xffffff)  # White LED
    time.sleep(1)
    pycom.rgbled(0x32CD32)  # LIMEGREEN LED
    time.sleep(1)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, True)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)
    s.send('H{}'.format(count))
    s.setblocking(False)
    data = s.recv(64)
    print(data)
    print(" Send data success....Entering sleep mode")
    pycom.heartbeat(True)
    time.sleep(send_interval * seconds)

# s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# # s.bind(5)
# s.setsockopt(socket.SOL_LORA, socket.SO_DR, 4)
# s.setsockopt(socket.SOL_LORA,  socket.SO_CONFIRMED,  True)
#
# cpt = 1
#
# while True:
#    pycom.rgbled(0x110000)
#    s.setblocking(True)
#    s.settimeout(30)
#
# # for testing new code, remove try/except
#
#    try:
#        print('sending', cpt)
#        s.send('Hello LoRa {}'.format(cpt))
#    except:
#        print ('timeout in sending')
#
#    pycom.rgbled(0x001100)
#
#    try:
#        data = s.recv(64)
#
#        print(data)
#        pycom.rgbled(0x000011)
#    except:
#        print ('timeout in receive')
#        pycom.rgbled(0x000000)
#
#
#    s.setblocking(False)
#    time.sleep (30)
#
#    cpt += 1

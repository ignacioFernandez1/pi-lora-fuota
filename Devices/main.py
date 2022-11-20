from network import LoRa
import socket
import time
import binascii
import pycom

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

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
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
    s.setblocking(True)
    s.send(bytes([0x11, 0x0E, 0xE2, 0x06, 0xBD, 0x06, 0x34, 0x34, 0x34, 0x00]))
    s.setblocking(False)
    data = s.recv(64)
    print(data)
    print(" Send data success....Entering sleep mode")
    pycom.heartbeat(True)
    time.sleep(send_interval * seconds)

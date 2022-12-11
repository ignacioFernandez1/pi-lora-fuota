from network import LoRa
import socket
import time
import binascii
import pycom
import struct

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C)

def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        print('RECEIVED A MESSAGE')
        if s is not None:
            frame, port = s.recvfrom(512) # longuest frame is +-220
            print(port, frame)
    if events & LoRa.TX_PACKET_EVENT:
        print("tx_time_on_air: {} ms @dr {}", lora.stats().tx_time_on_air, lora.stats().sftx)

dev_eui = binascii.unhexlify('c5c65c3303799380'.replace(' ', ''))
app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ', ''))
app_key = binascii.unhexlify('8754db1f30f53f908109cee5f62846e6'.replace(' ', ''))

# mcAddr = struct.unpack(">l", binascii.unhexlify('0053cd8f'))[0]
# mcNwkKey = binascii.unhexlify('F9CEFC8DC156D1CA0C61F664B1C84725')
# mcAppKey = binascii.unhexlify('01CF92D6F28A7F7A193647739059278C')
# print('joining multicast')
# lora.join_multicast_group(mcAddr, mcNwkKey, mcAppKey)
# print('joined multicast')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
print("devEUI {}".format(binascii.hexlify(lora.mac())))


pycom.heartbeat(False)
pycom.rgbled(0x111111)

print(lora.stats().tx_frequency)

while not lora.has_joined():
    time.sleep(1)
    print('.', end='')
print('Network joined!')

lora.callback(trigger=( LoRa.RX_PACKET_EVENT |
                        LoRa.TX_PACKET_EVENT |
                        LoRa.TX_FAILED_EVENT  ), handler=lora_cb)

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

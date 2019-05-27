#!/usr/bin/env python3

import time

from smartcard.scard import *
import smartcard.util

from ACR122_codes import *
import pcsc_utils

pcsc_utils.DEBUG_PRINT = True


# берём контекст
hres, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
pcsc_utils.check(hres, 'establish context')


# берём ридеры
hres, readers = SCardListReaders(hcontext, [])
pcsc_utils.check(hres, 'list readers')

if len(readers) < 1:
    raise Exception('No smart card readers')


# берём первый ридер и инициализируем состояние
reader = readers[0]
readerstates = [(reader, SCARD_STATE_UNAWARE)]
hres, readerstates = SCardGetStatusChange(hcontext, 0, readerstates)
pcsc_utils.check(hres, 'get status change')
print('Using reader:', reader)

print('Calibration Time!\n')


# если нет карты, то дожидаёмся её
while not pcsc_utils.insertedCardState(readerstates[0]):
    print("Place a tag on the device")
    timeout_calibration = 30 # 30 секунд?
    hres, readerstates = SCardGetStatusChange(hcontext, timeout_calibration, readerstates)
    pcsc_utils.check(hres, 'get status change')


# и отключаем стандартный биб, взяв коннект
hres, hcard, dwActiveProtocol = SCardConnect(hcontext, reader,
                            SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
pcsc_utils.check(hres, 'connect')

# отключаем биб
hres, response = SCardTransmit(hcard, dwActiveProtocol, DISABLE_STD_BUZZER)
pcsc_utils.check(hres, 'disable standart buzzer')

# и 2 раза бибикним
hres, response = SCardTransmit(hcard, dwActiveProtocol, BUZZING)
pcsc_utils.check(hres, 'init buzzing 1')

time.sleep(0.5)

hres, response = SCardTransmit(hcard, dwActiveProtocol, BUZZING)
pcsc_utils.check(hres, 'init buzzing 1')

# ожидаем освобождение ридера
while pcsc_utils.insertedCardState(readerstates[0]):
    print("Leave a tag from the device")
    timeout_calibration = 30 # 30 секунд?
    hres, readerstates = SCardGetStatusChange(hcontext, timeout_calibration, readerstates)
    pcsc_utils.check(hres, 'get status change')

print("Calibration is finished!")

while True:
    # TODO: а что с исключениями?
    # ждём карту
    hres, readerstates = SCardGetStatusChange(hcontext, INFINITE, readerstates)
    pcsc_utils.check(hres, 'get status change')
    pcsc_utils.printState(readerstates[0])

    # получаем tag
    hres, response = SCardTransmit(hcard, dwActiveProtocol, APDU)
    pcsc_utils.check(hres, 'get apdu')
    print("responce:", smartcard.util.toHexString(response, smartcard.util.HEX))

    # TODO: а что если ошибочка?

    # сообщаяем звуком
    hres, response = SCardTransmit(hcard, dwActiveProtocol, BUZZING)
    pcsc_utils.check(hres, 'ending buzzing')




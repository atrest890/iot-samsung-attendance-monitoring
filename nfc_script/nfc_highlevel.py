#!/usr/bin/env python3


from enum import Enum

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.scard import INFINITE

import ACR122_codes
import nfc_sender


class State(Enum):
    INIT = 0
    PROCESSING = 1
    ENDING = 2

def waitConnect(timeout=INFINITE, cardType=AnyCardType(), newcardonly=True):
    cardrequest = CardRequest(timeout=timeout, cardType=cardType, newcardonly=True)
    cardservice = cardrequest.waitforcard()
    return cardservice.connection



state = State.INIT

# init
while state == State.INIT:
    try:
        print("Calibration Time!")
        print("Place a tag on the device")
        conn = waitConnect()
        # TODO: а что по ошибкам?
        conn.connect()
        conn.transmit(ACR122_codes.DISABLE_STD_BUZZER)
        conn.transmit(ACR122_codes.BUZZING)
        conn.transmit(ACR122_codes.BUZZING)
        conn.disconnect()
        print("Calibration is finished!")
        print("Leave a tag from the device")
        state = State.PROCESSING
    except Exception as e:
        print(e)

#state = State.PROCESSING
sender = nfc_sender.NFCSender()
sender.start()

# main loop
while state == State.PROCESSING:
    try:
        print("Wait to card")
        conn = waitConnect(newcardonly=False)
        conn.connect()
        print("Connected, transmiting...")
        response, sw1, sw2 = conn.transmit(ACR122_codes.APDU)

        print("responce: ", response)
        if sw1 == 0x90 and sw2 == 0x00:
            sender.append(response)
        else:
            raise Exception( "Bad response on transmit[" + response + "], sw = " + str((hex(sw1), hex(sw2))) )

        print("Buzzing...")
        conn.transmit(ACR122_codes.BUZZING)
        conn.disconnect()
        print("Disconnected")
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        state = State.ENDING
    except InterruptedError:
        print("Interrupt")
        state = State.ENDING
    except Exception as e:
        print(e)

if state == State.ENDING:
    sender.stop()

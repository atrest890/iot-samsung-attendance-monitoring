#!/usr/bin/env python3

DISABLE_STD_BUZZER = [0xFF, 0x00, 0x52, 0x00, 0x00]
APDU = [0xFF, 0xCA, 0x00, 0x00, 0x04]
BUZZING = [0xFF, 0x00, 0x40, 0xCF, 0x04, 0x03, 0x00, 0x01, 0x01]

class PseudoAPDU:
    """
    Pseudo-APDU for ACR122U (section 6.0)  
    https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/

    Attributes:
        DIRECT_TRANSMIT_PREAMBLE - direct transmit command without 'Lc' and 'Data In'  (section 6.1)  
        BI_COLOR_LED_AND_BUZZER_CONTROL_PREABLE - preable of command control of led and buzzer (section 6.2)
    """
    # direct transmit
    DIRECT_TRANSMIT_PREAMBLE = [0xFF, 0x00, 0x00, 0x00]

    # led and buzzer
    BI_COLOR_LED_AND_BUZZER_CONTROL_PREABLE = [0xFF, 0x00, 0x40]

    
    

    def CreateDirectTransmit(self, dataIn: list):
        """Creates 'Direct Transmit' (section 6.1) with the data, the maximum size of 255"""
        assert(len(dataIn) < 255)
        return self.DIRECT_TRANSMIT_PREAMBLE + [len(dataIn)] + dataIn

    


#!/usr/bin/env python3

import threading
import time
import requests
import datetime
import json

import protocol
from traceback import print_exc

URL = 'http://192.168.43.193:8000/dategate'
ID = 'f2e50d503396c297d13284d7849c9846'

class NFCSender():
    """
    Задача NFCSender - отправлять на сервер nfc теги.
    """
    TIMER = 5 # секунды

    def __init__(self):
        self._listNFCs = []
        self._listTimestamp = []
        # self._thread = threading.Thread(self.__send)
        self._timer = self.__createTimer()
        self._hasStop = False
        self.prot = protocol.manager.getLastVersion()
        self._deltaDate = datetime.timedelta()        

    def __createTimer(self):
        return threading.Timer(self.TIMER, self.__send)

    def __sendImpl(self):
        data = self.prot.serializeNFC(ID, self._listNFCs, self._listTimestamp)

        try:
            if self._ses is None:
                self.__connect()

            print("Sending:", self._listNFCs)
            r = self._ses.post(URL, data=data)
            print("Sended:", r.status_code)
            self._listToSend = []
        except Exception:
            print_exc()
            self.__reconnect()

    def __send(self):
        if len(self._listToSend) != 0:
            self.__sendImpl()

        self._timer = self.__createTimer()
        if not self._hasStop:
            self.start()
        
    def __reconnect(self):
        print("Reconnecting...")
        self._ses = None
        self.__connect()

    def __connect(self):
        self._ses = requests.Session()
        r = self._ses.get(URL)
        print('Connection status =', r.status_code)

        cmd, serverDate = self.prot.deserialize(r.text)
        print('Command in answer:', cmd)

        self._deltaDate = serverDate - datetime.datetime.now()
        print('Delta time: ', self._deltaDate)        
        
        if r.status_code != 200:
            raise Exception('Connected failed, status code: ' + r.status_code)

    def __getCurrentTime(self):
        return (datetime.datetime.now() + self._deltaDate).timestamp()

    def start(self):
        self._hasStop = False
        self.__connect()
        self._timer.start()

    def stop(self):
        self._hasStop = True
        self._timer.cancel()

    def append(self, nfc):
        self._listNFCs.append(nfc)
        self._listTimestamp.append(self.__getCurrentTime())

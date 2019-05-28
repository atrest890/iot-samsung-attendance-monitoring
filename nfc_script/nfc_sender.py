#!/usr/bin/env python3

import threading
import time

class NFCSender():
    """
    Задача NFCSender - отправлять на сервер nfc теги.
    """
    TIMER = 30 # секунды

    def __init__(self, ip, port):
        self._listToSend = []
        # self._thread = threading.Thread(self.__send)
        self._timer = self.__createTimer()
        self._hasStop = False

    def __createTimer(self):
        return threading.Timer(self.TIMER, self.__send)

    def __send(self):
        localList = self._listToSend
        self._listToSend = []
        
        for i in localList:
            print("Sending", i, "...")
            print("ERROR: Sending not impl")
            print("Sended [", 404, ']')

        self._timer = self.__createTimer()
        if not self._hasStop:
            self.start()
        
    def start(self):
        self._hasStop = False
        self._timer.start()

    def stop(self):
        self._hasStop = True
        self._timer.cancel()

    def append(self, nfc):
        self._listToSend.append(nfc)
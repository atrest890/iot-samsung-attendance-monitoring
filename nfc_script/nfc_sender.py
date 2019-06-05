#!/usr/bin/env python3

import threading
import time
import requests
import datetime
import json

URL = '192.168.43.193:8000/dategate'
ID = 'f2e50d503396c297d13284d7849c9846'

class NFCSender():
    """
    Задача NFCSender - отправлять на сервер nfc теги.
    """
    TIMER = 30 # секунды

    def __init__(self):
        self._listToSend = []
        # self._thread = threading.Thread(self.__send)
        self._timer = self.__createTimer()
        self._hasStop = False

    def __createTimer(self):
        return threading.Timer(self.TIMER, self.__send)

    def __sendImpl(self):
        data = json.dumps((ID, self._listToSend))

        try:
            print("Sending:", self._listToSend)
            r = self._ses.post(URL, json=data)
            print("Sended:", r.status_code)
            self._listToSend = []
        except Exception as e:
            print("Exception!")
            print(e)


    def __send(self):
        if len(self._listToSend) != 0:
            self.__sendImpl()

        # self._timer = self.__createTimer()
        if not self._hasStop:
            self.start()
        
    def __connect(self):
        self._ses = requests.Session()
        r = self._ses.get(URL)
        self._deltaDate = datetime.datetime.fromtimestamp(r.text()) - datetime.datetime.now()
        print('Connection status =', r.status_code)
        
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
        self._listToSend.append((nfc, self.__getCurrentTime()))
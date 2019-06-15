#!/usr/bin/env python3

import json
import datetime
from typing import List, Tuple

class ProtocolBase():
    VERSION = "0"

    def __init__(self):
        self._deserHanglers = {}    

    @staticmethod
    def to_data(data: dict) -> str:
        payload = json.dumps(data['data'], allow_nan=False)
        return f"{data['version']}^{data['cmd']}^{payload}"

    @staticmethod
    def from_data(data: str) -> dict:
        parts = data.split('^')
        return {
            "version" : parts[0],
            "cmd" : parts[1],
            "data" : json.loads(parts[2])
        }

    def _serialize(self, cmd, **kwargs) -> str:
        return self.to_data({
                "version" : self.VERSION,
                "cmd" : cmd,
                "data" : kwargs
            })

    def deserialize(self, data):
        """
            Десериализация входящих данных, возвращает команду и данные.

            В случае несоответсвии версии поднимает версию или бросает исключение
        """
        obj = self.from_data(data)

        version = obj["version"]
        if version != self.VERSION:
            # TODO: а точно нужно такое поведение?
            global manager
            if version in manager:
                return manager[version].__deserialize(data)
            else:
                raise Exception(f"Version not supported. v: {version}")

        cmd = obj["cmd"]
        if cmd in self._deserHanglers:
            return cmd, self._deserHanglers[cmd](obj["data"])

        raise Exception(f"Command not supported. v: {self.VERSION}, cmd: {cmd}")


class Protocol_0_1(ProtocolBase):
    VERSION = "0.1"

    # command
    NFCs_PROCESS = "nfs_process"
    DATE_REQUEST = "date_request"
    DATE_RESPONSE = "date_response"

    def __init__(self):
        super().__init__()
        self._deserHanglers[self.NFCs_PROCESS] = self.deserializeNFC
        self._deserHanglers[self.DATE_REQUEST] = self.deserializeStub
        self._deserHanglers[self.DATE_RESPONSE] = self.deserializeDateResponse

    def deserializeStub(self, *args, **kwargs):
        """
            Заглушка для пустых обработчиков, возвращают None
        """
        return None

    def serializeNFC(self, idDevice : str, listNFCs : List[List[int]], listTimestamp : List[float] = None) -> str:
        """
            Сериализует список тегов и соответствующих дат в строку, подходящую для отправки и десериализации протоколом.
        """
        if listTimestamp is not None and len(listTimestamp) != len(listNFCs):
            raise Exception("The number of tags and dates does not match")
        
        dataList = []
        for idx, nfs in enumerate(listNFCs):
            # now() or input timestamp
            if listTimestamp is None or listTimestamp[idx] is None:
                date = datetime.datetime.now().timestamp()
            else:
                date = listTimestamp[idx]

            if type(date) == datetime.datetime:
                date = date.timestamp()
            if type(date) != float:
                raise Exception("listDate contains not float timestamp")

            if type(nfs) == list:
                nfs = bytes(nfs)
            if type(nfs) == bytes:
                nfs = nfs.hex()
            if type(nfs) != str:
                raise Exception("listNFCs contains not list of int or bytes or str")

            dataList.append( (nfs, date) )

        return self._serialize(self.NFCs_PROCESS, id=idDevice, data=dataList)

    def deserializeNFC(self, obj: dict) -> Tuple[str, List[Tuple[bytes, datetime.datetime]]]:
        """
            Десериализует входящий объект, возвращает тупл из id устройства и списка туплов из тега и datetime
        """
        idDevice = obj["id"]
        dataList = []
        for item in obj["data"]:
            nfs = bytes.fromhex(item[0])
            date = datetime.datetime.fromtimestamp(item[1])

            dataList.append( (nfs, date) )

        return idDevice, dataList

    def serializeDateRequest(self):
        """
            Формирует запрос на дату сервера
        """
        return self._serialize(self.DATE_REQUEST)

    def serializeDateResponce(self, date: datetime) -> str:
        """
            Формирует ответ с переданной или текущуй датой
        """

        if date is None:
            date = datetime.datetime.now()
        if type(date) is datetime.datetime:
            date = date.timestamp()

        return self._serialize(self.DATE_RESPONSE, date=date)

    def deserializeDateResponse(self, obj : dict) -> datetime:
        """
            Парсит данные и возвращает время сервера
        """
        return datetime.datetime.fromtimestamp(obj["date"])


class ProtocolManager(dict):
    def __init__(self):
        super().__init__()
        
        self[ProtocolBase.VERSION] = ProtocolBase()
        self[Protocol_0_1.VERSION] = Protocol_0_1()

    def getLastVersion(self) -> Protocol_0_1:
        return self[Protocol_0_1.VERSION]

    def parseVersion(self, data):
        return data.split('^')[0]


manager = ProtocolManager()


    
ID = "222222222"
nfcs = [[0x11, 0x22], [0x33, 0x44]]
dates = None

# prot = manager.getLastVersion()

# with open('/tmp/json.json', 'w') as f:
#     j = prot.serializeNFC(ID, nfcs, dates)
#     f.write( j )

#     print(prot.deserialize(j))
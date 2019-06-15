#!/usr/bin/env python3

import unittest
import datetime

class TestProtocol_0_1(unittest.TestCase):

    def test_nfsSerFull(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        ID = "222222222"
        nfcs = [[0x11, 0x22], [0x33, 0x44]]
        dates = [ datetime.datetime(2019, 6, 15, 14, 23, 21, 787773), datetime.datetime(2019, 6, 15, 14, 23, 21, 787799) ]

        s = prot.serializeNFC(ID, nfcs, dates)
        data = '0.1^nfs_process^{"id": "222222222", "data": [["1122", 1560583401.787773], ["3344", 1560583401.787799]]}'
        self.assertEqual(s, data)

    def test_nfsDeserFull(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        data = '0.1^nfs_process^{"id": "222222222", "data": [["1122", 1560583401.787773], ["3344", 1560583401.787799]]}'
        
        cmd, content = prot.deserialize(data)
        self.assertEqual(cmd, 'nfs_process')

        device, checkins = content
        self.assertEqual(device, '222222222')
        checkins_correct = [(b'\x11"', datetime.datetime(2019, 6, 15, 14, 23, 21, 787773)), (b'3D', datetime.datetime(2019, 6, 15, 14, 23, 21, 787799))]
        self.assertEqual(checkins, checkins_correct)

    def test_dateSerReq(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        s = prot.serializeDateRequest()
        self.assertEqual(s, '0.1^date_request^{}')

    def test_dateDeserReq(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        data = '0.1^date_request^{}'

        ans = prot.deserialize(data)
        self.assertTupleEqual(ans, ('date_request', None))

    def test_dateSerResp(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        now = datetime.datetime.now()

        s = prot.serializeDateResponce(now)
        self.assertEqual(s, '0.1^date_response^{"date": ' + str(now.timestamp()) +'}' )

    def test_dateDeserResp(self):
        import protocol as p
        prot = p.manager[p.Protocol_0_1.VERSION]

        data = '0.1^date_response^{"date": 1560585604.541747}'
        ans = prot.deserialize(data)
        self.assertTupleEqual(ans, ('date_response', datetime.datetime(2019, 6, 15, 15, 0, 4, 541747)))

if __name__ == '__main__':
    unittest.main(verbosity=2)

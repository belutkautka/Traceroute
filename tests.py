import unittest
from UDP_traceroute import Tracerouter
import traceroute_algo
class TestUDP(unittest.TestCase):
    def setUp(self):
        pass
    def test_udp(self):
        data=[]
        base=traceroute_algo.udp("172.217.23.78", 53, 2, 3,0,True)
        tracer=Tracerouter("172.217.23.78",53,2,3,0,False,data,40)
        data = tracer.run()
        self.assertEqual(len(base)-1,len(data))
        for i in range(len(data)):
            self.assertEqual(base[i+1][1], data[i][1])

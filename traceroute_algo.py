from scapy.config import conf
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest
from scapy.sendrecv import sr1
from texttable import Texttable
import time
from UDP_traceroute import Tracerouter


def is_found(pkt, ip, timeout, requests,data):
    conf.verb = 0
    start = time.time()
    response = sr1(pkt, timeout=timeout)
    finish = time.time()
    times = round((finish - start) * 1000)
    if not response:
        pass
        #print(f'{requests} *')
    else:
        ip_res = response.src
        data.append([str(requests),ip_res,f'{times} ms'])
        if ip == ip_res:
            return True
    return False


def icmp(ip, timeout, requests,sendwait):
    ttl = 1
    data = [['Номер запроса', 'IP', 'Время ответа']]
    while ttl <= requests:
        if ':' in ip:
            pkt = IPv6(dst=ip, hlim=ttl) / ICMPv6EchoRequest()
        else:
            pkt = IP(dst=ip, ttl=ttl) / ICMP()
        if is_found(pkt, ip, timeout, ttl,data):
            break
        time.sleep(sendwait)
        ttl += 1
    make(data)

def tcp(ip, port, timeout, requests,sendwait):
    ttl = 1
    data=[['Номер запроса', 'IP','Время ответа']]
    while ttl <= requests:
        if ':' in ip:
            pkt = IPv6(dst=ip, hlim=ttl) / TCP(dport=port)
        else:
            pkt = IP(dst=ip, ttl=ttl) / TCP(dport=port)
        if is_found(pkt, ip, timeout, ttl,data):
            break
        time.sleep(sendwait)
        ttl += 1
    make(data)
def udp_socket(ip,port,timeout,request,sendwait,debug,size):
    data=[['Номер запроса', 'IP', 'Время ответа']]
    tracerouter=Tracerouter(ip,port,timeout,request,sendwait,debug,data,size)
    data=tracerouter.run()
    make(data)
def udp(ip, port, timeout, requests,sendwait,test=False):
    ttl = 1
    data = [['Номер запроса', 'IP', 'Время ответа']]
    while ttl <= requests:
        if ':' in ip:
            pkt = IPv6(dst=ip, hlim=ttl) / UDP(dport=port)
        else:
            pkt = IP(dst=ip, ttl=ttl) / UDP(dport=port)
        if is_found(pkt, ip, timeout, ttl,data):
            break
        time.sleep(sendwait)
        ttl += 1
    if not test:
        make(data)
    else: return data
def make(data):
    t = Texttable()
    t.add_rows(data)
    print(t.draw())



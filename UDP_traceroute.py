import socket
import time
#traceroute.py 172.217.23.78 udp -p 53 -n 3 -d
class Tracerouter:
    def __init__(self, ip,port,timeout,request,sendwait,debug,data,size):
        self.ip = ip
        self.request = request
        self.timeout = timeout
        self.port = port
        self.sendwait = sendwait
        self.debug = debug
        self.data=data
        self.size=size

    def log(self,message):
        if self.debug:
            with open('logs.txt', "a") as file:
                file.write(message + "\n")

    def send_and_recive(self, send_socket, recv_socket):
        self.log(f'Отправка на {self.ip}')
        send_socket.sendto(b"0" * self.size ,(self.ip, self.port))
        adr = ''
        try:
            _, adr = recv_socket.recvfrom(512)
            adr = adr[0]
            self.log(f'Получение данных от {adr}')
        except socket.timeout as e:
            self.log(f'Вышло время ожидания ответа')
            pass
        return adr

    def ping(self, ttl, send_socket, recv_socket):
        recv_socket.settimeout(self.timeout)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        current = None
        start = time.time()
        adr = self.send_and_recive(send_socket,recv_socket)
        if adr != '':
            current = adr
        times = round((time.time() - start) * 1000)
        self.log(f'Время ответа {times} ms')
        return current,times

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname("udp")) as send_socket:
            with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp")) as recv_socket:
                for ttl in range(1, self.request + 1):
                    self.log(f'Отправка пакета на {self.ip} с ttl {ttl}')
                    current,times= self.ping(ttl, send_socket, recv_socket)
                    if current is None:
                        continue
                    else:
                        self.data.append([str(ttl), current, f'{times} ms'])
                    if current == self.ip:
                        break
                    time.sleep(self.sendwait)
        return self.data

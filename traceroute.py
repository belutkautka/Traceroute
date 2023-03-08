import argparse
import traceroute_algo
from sys import platform


def inp():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', dest="timeout", help="Таймаут ожидания ответа", type=int, default=2)
    parser.add_argument('-s', '--packet_size', dest="packet_size", help="Размер отправляемого пакета (только для UDP в режиме сокета)", type=int, default=40)
    parser.add_argument('-p', '--port', dest="port", help="Порт (для TCP/UDP)", type=int)
    parser.add_argument('-n', '--hops', dest="requests", help="Максимальное количество запросов", type=int, default=30)
    parser.add_argument('-d', '--debug', dest="debug", help="Режим дебага (только для UDP в режиме сокета)", action="store_true", default=False)
    parser.add_argument('-sk', '--socket', dest="socket", help="Режим сокета (только для UDP на Linux с правами)", action="store_true",
                        default=False)
    parser.add_argument('-z', '--sendwait', dest="sendwait", help="Интервал времени между запросами", type=int, default=0)
    parser.add_argument('ip', help="IP адрес")
    parser.add_argument('protocol', help="TCP/UDP/ICMP", choices=['tcp', 'udp', 'icmp'])
    return parser


def traceroute():
    arguments = inp().parse_args()
    ip = arguments.ip
    port = arguments.port
    time = arguments.timeout
    requests = arguments.requests
    debug=arguments.debug
    size=arguments.packet_size
    socket=arguments.socket
    sendwait=arguments.sendwait
    if arguments.protocol == "tcp":
        traceroute_algo.tcp(ip, port, time, requests,sendwait)

    elif arguments.protocol == "udp":
        if socket:
            if platform == "linux" or platform == "linux2":
                try:
                    traceroute_algo.udp_socket(ip, port, time, requests, sendwait, debug, size)
                except:
                    print("Для запуска режима сокета необходим запуск пргораммы с правами")
            else:
                print("Режим сокета для UDP можно запускать только на линуксе")
        else:
            traceroute_algo.udp(ip, port, time, requests,sendwait)
    elif arguments.protocol == "icmp":
        traceroute_algo.icmp(ip, time, requests,sendwait)


if __name__ == "__main__":
    traceroute()

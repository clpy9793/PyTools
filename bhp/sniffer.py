import time
import socket
import struct
import logging
import datetime
import traceback
import threading
from ctypes import *
from netaddr import IPNetwork, IPAddress

logging.basicConfig(level=logging.DEBUG)

PROTOCOL_MAP = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
}


IPH_FMT = """
协议版本: ipv{ip_v}
头长度: {ip_hl}
服务类型: {ip_tos}
IP 数据包总长: {ip_len}
标识符: {ip_id}
标记: {ip_identity}
片偏移: {ip_off}
生存时间: {ip_ttl}
协议类型: {ip_p}
头部校验: {ip_sum}
源地址: {ip_src}
目的地址: {ip_dst}
"""

IPB_FMT = """
类型值: {ipb_type}
代码值: {ipb_code}
检验和: {ipb_checksum}
"""


def get_host_ip():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return host_ip


def bind_addr():
    host_ip = get_host_ip()
    socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    while True:
        data, _ = sniffer.recvfrom(65536)
        r = parse_header(data)
        src = r['ip_src']
        dst = r['ip_dst']
        if r['ip_p'] == 'ICMP':
            iph_len = r['ip_hl']
            offset = iph_len * 4
            r = parse_icmp(data[offset:])
            if r['ipb_code'] == r['ipb_type'] == 3:
                if 'test message'.encode() in data:
                    logging.info("Host up: {}".format(src))


def parse_header(data):
    offset = 0
    ch = data[offset]
    ip_v = ch >> 4
    ip_hl = ch & 0b1111

    offset += 1
    ip_tos = data[offset]

    offset += 1
    rg = slice(offset, offset+2)
    ip_len = struct.unpack('<H', data[rg])[0]

    offset = 4
    rg = slice(offset, offset+2)
    ip_id = struct.unpack('<H', data[rg])[0]

    offset = 4 + 2
    rg = slice(offset, offset+2)
    tmp = struct.unpack('<H', data[rg])[0]
    ip_identity = tmp >> 14
    ip_off = tmp & 2**14-1

    offset = 8
    rg = slice(offset, offset + 1)
    ip_ttl = struct.unpack('<B', data[rg])[0]

    offset = 8 + 1
    rg = slice(offset, offset + 1)
    ip_p = struct.unpack('<B', data[rg])[0]
    ip_p = PROTOCOL_MAP[ip_p]

    offset = 8 + 2
    rg = slice(offset, offset + 2)
    ip_sum = struct.unpack('<H', data[rg])[0]

    offset = 12
    rg = slice(offset, offset + 4)
    ip_src = socket.inet_ntoa(data[rg])

    offset = 16
    rg = slice(offset, offset + 4)
    ip_dst = socket.inet_ntoa(data[rg])
    return locals()


def parse_icmp(data,):
    offset = 0
    ipb_type = data[offset]

    offset += 1
    ipb_code = data[offset]

    offset += 1
    rg = slice(offset, offset + 2)
    ipb_checksum = struct.unpack('<H', data[rg])[0]
    return locals()


def udp_sender(subnet, msg):
    time.sleep(2)
    port = 65212
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        addr = (str(ip), port)
        try:
            sock.sendto(msg, addr)
        except PermissionError:
            pass
        except:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    subnet = '{}/24'.format(get_host_ip())
    t = threading.Thread(target=udp_sender, args=(
        subnet, 'test message'.encode()))
    t.start()
    bind_addr()

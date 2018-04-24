import os
import socket
import datetime
import struct
from ctypes import *

PROTOCOL_MAP = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
}


def bind_addr():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    while True:
        data, _ = sniffer.recvfrom(65536)
        r = parse(data)
        print(r['s'])


def parse(data):
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

    s = """
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
    """.format(**locals())
    return locals()


if __name__ == '__main__':
    bind_addr()

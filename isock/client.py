# import os
# import time
# import socket


# if __name__ == '__main__':
#     address = ('127.0.0.1', 9793)
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(address)
#     s.send(b'hihi')
#     s.send(b'hihi')
#     s.close()
import socket
import socks
import requests
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9793)
socket.socket = socks.socksocket
requests.get("http://www.ush360.com")

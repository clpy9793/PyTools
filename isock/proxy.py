#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-17 15:07:55
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import asyncio


async def handle_client(reader, writer):
    # Version
    data = await reader.read(258)
    if data[:2] != b'\x05\x01':
        print('无效请求', data)
    writer.write(b'\x05\x00')

    # Request
    ver, cmd, rev, atyp = await reader.read(4)
    print(ver, cmd, rev, atyp, sep=' ')
    if cmd == 1:    # Connect
        pass
    elif cmd == 2:  # Bind
        pass
    elif cmd == 3:  # Udp
        pass
    else:
        print('invaild request cmd: {cmd}')
    print('close')
    writer.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_client, '127.0.0.1', 9793, loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

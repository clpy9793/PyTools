#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-07 16:29:42
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://119.29.97.218:8000/wzgj/') as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())

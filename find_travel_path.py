import os
import asyncio
import trio
import aiohttp


API_KEY = "5f5b3f610f29f236a26e487e6fdeba9e"
RESULT = {}
ADDRESS = ""


async def start():
    stop_list = await find_near_bus_stop()

async def find_near_bus_stop():
    el = asyncio.get_event_loop()
    el.create_task(get_bus_list())


async def get_bus_list():
    print(1)


async def each_bus_stop():
    pass


async def calc_distance():
    pass


if __name__ == '__main__':
    trio.run(start)

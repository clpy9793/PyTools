import random
import logging
import asyncio
import traceback
import aiohttp

L_FORMAT = '%(asctime)-15s %(levelname)s %(lineno)d %(funcName)s %(message)s'
basic_config = dict(
    format=L_FORMAT,
    level=logging.DEBUG,
    handlers=[logging.FileHandler('./qg.log', 'w', 'utf-8'), ],
)
logging.basicConfig(**basic_config)

API_HOST = 'api.v3.iqianggou.com'
API_URL = "http://{}/api/item".format(API_HOST)
SUCCESS_CODE = 10000
SUCCESS_MSG = '成功'
REQ_WAIT_LIST = [1, 5]

QS = {
    'category_id': '0',
    'channel': 'AppStore',
    'last_id': '0',
    'lat': '31.131477',
    'latitude': '31.131477',
    'lng': '121.549290',
    'longitude': '121.549290',
    'udid': 'db78dbed562c4311fd25fff899b45c2b8f32d11a',
    'user_id': '7067493',
    'version': '5.3.3',
    'zone_id': '21'
}


async def start():
    try:
        async with aiohttp.ClientSession() as session:
            qs = QS.copy()
            has_more = True
            count = 0
            page = 1
            while has_more:
                async with session.get(API_URL, params=qs) as resp:
                    res = await resp.json()
                    status = res['status']
                    if (status['code'] != SUCCESS_CODE or
                            status['message'] != SUCCESS_MSG):
                        logging.error(await resp.text(encoding='utf8'))
                    count += len(res['data'])
                    await parse(res['data'])
                    pagination = res['pagination']
                    has_more = pagination['has_more']
                    qs['last_id'] = pagination['last_id']
                    wait = random.choice(REQ_WAIT_LIST)
                    logging.info("page %d done.", page)
                    page += 1
                    await asyncio.sleep(wait)

        logging.info('have no more data.')
        logging.info("total count: %d", count)
        logging.info('Done\n\n')
    except Exception:
        logging.error(traceback.format_exc())


async def parse(data):
    # Todo: parse item and save to local storage
    pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()

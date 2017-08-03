#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-02 15:28:21
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import random
import asyncio
import requests
import aiohttp
import aiofiles
from traceback import format_exc
from pyquery import PyQuery as pq
try:
    import ujson as json
except ImportError:
    import json

host = 'http://xyq.cbg.163.com'
url = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?j5up3b8v&level_min=109&level_max=109&expt_total=68&bb_expt_total=68&skill_qiang_shen=129&skill_shensu=36&skill_qiang_zhuang=36&act=overall_search_role&page={0}'
equipquery = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid={serverid}&ordersn={ordersn}'
# equipquery = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid=127&ordersn=280_1501152627_282072511&equip_refer=10'

RESULT = []

def main():
    pages = [url.format(i) for i in range(1, 10)]
    tasks = [parse_first_page(i) for i in pages]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

async def parse_first_page(page):
    async with aiohttp.ClientSession() as session:
        res = await session.get(page)
        ret = await res.text(encoding='utf8')
        ret = json.loads(ret)
        if 'equip_list' not in ret:
            print(ret)
            return
        for item in ret['equip_list']:
            tmp = {}
            tmp['serverid'] = item['serverid']
            tmp['ordersn'] = item['game_ordersn']
            detail_page = equipquery.format(**tmp)
            detail = await session.get(detail_page)
            # print(detail_page)
            content = await detail.text(errors='ignore')
            doc = pq(content)
            text = doc('#equip_desc_value').text()
            equip_data = parse_text(text)
            equip_data = eval(equip_data)
            await parse_attack(equip_data, detail_page)
            await asyncio.sleep(5)
        return 


def parse_text(s):
    """解析混淆字符串"""
    s = s.replace('\n', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('[', '(')
    s = s.replace(']', ')')
    s = s.replace('{', '[')
    s = s.replace('}', ']')
    s = s.replace('(', '{')
    s = s.replace(')', '}')
    return s


async def parse_attack(data, url):
    """读取伤害"""
    #print(data['AllEquip'][2]['cDesc'])
    global RESULT
    if 6 not in data['AllEquip']:
        return
    raw_text = data['AllEquip'][6]['cDesc']
    text = raw_text.split('#r')
    attack = text[3].split(' ')
    attack = [i.replace('+', '') for i in attack]
    attack_num = int(attack[1]) + int(attack[3])/3.0
    # print(attack_num, url)
    extra_attack = 0
    stone = 0
    if '宝石' in text[5]:
        stone = int(text[5].split(' ')[1])
        if stone < 10:
            extra_attack = 3.3 * (10 - stone)
    attack_total = attack_num + extra_attack
    if attack_total >= 640:
        print(url)
        path = 'cbg_result.txt'
        async with aiofiles.open(path, 'a+', encoding='utf8') as f:
            await f.write(content.encode('utf8'))

    # print(url)
    # print(attack, attack_num, attack_total)



if __name__ == '__main__':
    main()

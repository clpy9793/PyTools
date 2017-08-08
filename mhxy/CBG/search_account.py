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
import traceback
from traceback import format_exc
from pyquery import PyQuery as pq
try:
    import ujson as json
except ImportError:
    import json

host = 'http://xyq.cbg.163.com'
url = 'http://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?j5w7y1yx&level_min=109&level_max=109&expt_total=68&bb_expt_total=68&skill_qiang_shen=129&act=overall_search_role&page={0}'
equipquery = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid={serverid}&ordersn={ordersn}'
# equipquery = 'http://xyq.cbg.163.com/cgi-bin/equipquery.py?act=overall_search_show_detail&serverid=127&ordersn=280_1501152627_282072511&equip_refer=10'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": '1',
    "Host": "xyq.cbg.163.com",
    "Proxy-Connection": "keep-alive",
}
cookie = "usertrack=c+xxClk/nMWwqx6gA0c6Ag==; _ntes_nnid=56ccb8d12c2809749e5e3c95057ab2e3,1497341097197; _ntes_nuid=56ccb8d12c2809749e5e3c95057ab2e3; _ga=GA1.2.1655429040.1497341099; __s_=1; P_INFO=1753166645@qq.com|1501476903|0|urs|11&11|shh&1501423110&urs#shh&null#10#0#0|&0|xyq&urs|1753166645@qq.com; no_login_mark=1; fingerprint=3395941467; overall_sid=EhTV8RwQz1T6_e6ZlQQ_Kgo6v6Ihkh1acqk6gaZa"
cookies = {
    'cookies': cookie.split(';')
}

RESULT = []

# 验证码
# 验证码获取链接
# http://xyq.cbg.163.com/cgi-bin/create_validate_image.py?act=search_captcha
# GET /cgi-bin/create_validate_image.py?act=search_captcha&stamp=0.6256550489234087 HTTP/1.1
# 验证码验证链接
# http://xyq.cbg.163.com//cgi-bin/equipquery.py?act=check_search_cpatcha&captacha=hdska
# 0成功 3失败
validate_url = 'http://xyq.cbg.163.com//cgi-bin/equipquery.py?act=check_search_cpatcha&captacha={captacha}'


def main():
    # pages = [url.format(i) for i in range(1, 10)]
    # tasks = [parse_first_page(i) for i in pages]
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(*tasks))
    loop.run_until_complete(start())
    loop.close()


async def parse_first_page(page):
    async with aiohttp.ClientSession(cookies=cookies) as session:
        res = await session.get(page, headers=headers)
        ret = await res.text(encoding='utf8')
        ret = json.loads(ret)
        if 'equip_list' not in ret:
            return False
        if len(ret['equip_list']) == 0:
            return False
        for item in ret['equip_list']:
            tmp = {}
            tmp['serverid'] = item['serverid']
            tmp['ordersn'] = item['game_ordersn']
            price = item['price']
            detail_page = equipquery.format(**tmp)
            detail = await session.get(detail_page)
            # print(detail_page)
            content = await detail.text(errors='ignore')
            doc = pq(content)
            text = doc('#equip_desc_value').text()
            equip_data = parse_text(text)
            equip_data = eval(equip_data)
            await parse_attack(equip_data, detail_page, price)
            await asyncio.sleep(1)
        return True

async def start():
    for i in range(1, 100):
        page = url.format(i)
        print('Page:\t', i)
        try:
            ret = await parse_first_page(page)
            if ret:
                await asyncio.sleep(2)
            else:
                break
        except:
            traceback.print_exc()
            continue

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



async def parse_attack(data, url, price):
    """读取伤害"""
    # print(data['AllEquip'][2]['cDesc'])
    global RESULT
    if 6 not in data['AllEquip']:
        return
    raw_text = data['AllEquip'][6]['cDesc']
    text = raw_text.split('#r')
    attack = text[3].split(' ')
    attack = [i.replace('+', '') for i in attack]
    if '伤害' in attack[0]:
        attack_num = int(attack[1]) + int(attack[3]) / 3.0
    elif '命中' in attack[0]:
        attack_num = int(attack[3]) + int(attack[1]) / 3.0
    else:
        print(attack)
        raise ValueError(attack)
    # print(attack_num, url)
    extra_attack = 0
    stone = 0
    if '宝石' in text[5]:
        stone = int(text[5].split(' ')[1])
        if stone < 10:
            extra_attack = 3.3 * (10 - stone)
    attack_total = attack_num + extra_attack
    if attack_total >= 650:
        print(url)
        path = 'cbg_result.txt'
        content = " ".join([str(attack_total), price, url, '\n'])
        async with aiofiles.open(path, 'a+') as f:
            await f.write(content)



if __name__ == '__main__':
    main()

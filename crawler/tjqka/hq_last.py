# coding: utf-8

import requests
import json
from marshmallow import Schema, fields

host = 'd.10jqka.com.cn'
referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/50.0.2661.102 ' \
             'Safari/537.36'

index_hq_url = 'http://d.10jqka.com.cn/v2/realhead/zs_{code}/last.js'
stock_url = 'http://d.10jqka.com.cn/v2/realhead/{market}_{code}/last.js'


class HQ(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    pre_close = fields.Decimal(load_from='6', places=3)
    open = fields.Decimal(load_from='7', places=3)
    high = fields.Decimal(load_from='8', places=3)
    low = fields.Decimal(load_from='9', places=3)
    close = fields.Decimal(load_from='10', places=3)
    volume = fields.Decimal(load_from='13', places=0)
    amount = fields.Decimal(load_from='19', places=3)
    change = fields.Decimal(load_from='264648', places=3)
    change_percent = fields.Decimal(load_from='199112', places=2)
    bid_ask_ratio = fields.Decimal(load_from='461256', places=2)
    bid_ask_diff = fields.Decimal(load_from='395720', places=0)
    in_size = fields.Decimal(load_from='15', places=0)
    out_size = fields.Decimal(load_from='14', places=0)


def hq_last(market, code, index=False):
    if index:
        if code == '000001':
            code = '1A0001'
        elif code == '000300':
            code = '1B0300'
        elif code == '000003':
            code = '1A0003'
        elif code == '000016':
            code = '1B0016'
        url = index_hq_url.format(code=code)
    else:
        url = stock_url.format(market=market, code=code)

    # Fake headers. Necessery?
    headers = {
        'Host': host,
        'Referer': referer,
        'User-Agent': user_agent
    }
    resp = requests.get(url, headers=headers)

    content = resp.content
    text = content[content.find('(')+1:content.rfind(')')]
    obj = json.loads(text)

    schema = HQ()
    result = schema.load(obj['items'])
    return result.data


if __name__ == '__main__':
    result = hq_last('sh', '600035', index=False)
    for k, v in result.iteritems():
        print k, v
    # result = hq_last('1A0001')

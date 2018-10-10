import requests
import json
from time import time, sleep
from re import search
import logging
from config import *



class Ym_api:
    url = "http://api.fxhyd.cn/UserInterface.aspx"
    token = YM_TOKEN
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}


    def __init__(self, itemid):
        self.itemid = itemid
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)



    # 获取token

    def get_token(self, username, password):

        params = {"action": "login", "username": username, "password": password}
        url = 'http://api.fxhyd.cn/UserInterface.aspx'
        content = requests.get(self.url, headers=self.headers, params=params).text
        # success|0073481819664ac5ccb1a6c9045ee42783e23d5e
        if content.split('|')[0] == 'success':
            token = content.split('|')[1]
            return token
        else:
            print("异常代码：", content)

    # 获取账户信息
    def get_account(self):

        params = {"action": "getaccountinfo", "token": self.token, "format": "1"}
        content = requests.get(self.url, headers=self.headers, params=params).text
        # success|{"UserName":"1574944154","UserLevel":1,"MaxHold":20,"Discount":1.000,"Balance":9.5000,"Status":1,"Frozen":10.0000}
        if content.split('|')[0] == 'success':
            account = content.split('|')[1]
            return json.loads(account)
        else:
            print("错误代码：", content)

    # 获取电话号码
    def get_mobile(self, excludeno=''):
        params = {"action": "getmobile", "token": self.token, "itemid": self.itemid, "excludeno": excludeno}
        content = requests.get(self.url, headers=self.headers, params=params).text
        if content.split('|')[0]  == 'success':
            mobile = content.split('|')[1]
            self.logger.info("获取到手机号码{}".format(str(mobile)))
            return str(mobile)
        else:
            print("错误代码：", content)

    # 释放号码
    def remove_mobile(self, mobile):
        params = {"action": "release", "token": self.token, "itemid": self.itemid, "mobile": mobile}
        content = requests.get(self.url, headers=self.headers, params=params).text
        if content == 'success':
            return content
        else:
            return 'false'

    def get_text(self, mobile, timeout=200):
        params = {"action": "getsms", "token": self.token, "itemid": self.itemid, "mobile": mobile, "release": "1"}
        t = time()
        while(time()-t < timeout):
            res = requests.get(self.url, headers=self.headers, params=params)
            res.encoding = "utf-8"
            content = res.text
            if content.split('|')[0] == 'success':
                num = search("【哔哩哔哩】(.*?) 为您的注册验证码", content.split('|')[1])
                return num.group(1)
            else:
                self.logger.info("{}未找到".format(time()-t))
                sleep(5)
        return 'flase'

if __name__ == '__main__':
    # print(remove_mobile(883,15843582274))
    # print(Ym_api(itemid='1191').get_token('1574944154', 'a510b63051ym'))
    ym = Ym_api(itemid='1191')
    num = ym.get_mobile()
    print(num)
    print(ym.get_text(num, timeout=500))
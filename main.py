# -*- coding: utf-8 -*-
import requests
import json
from urllib import parse
import re
from requests import cookies

from requests.models import Response


class netword():
    def __init__(self, useid, password):
        self.useid = useid
        self.password = password

    def Login(self):
        self.head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "Origin": self.ip,
                     "Referer": self.url,
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}

        self.cookie_JSESS["EPORTAL_COOKIE_OPERATORPWD"] = ""

        data = {"userId": self.useid,
                "password": self.password,
                "service": "",
                "operatorPwd": "",
                "operatorUserId": "",
                "validcode": "",
                "passwordEncrypt": "false",
                "queryString": self.deviceidencode
                }

        r = requests.post("http://" + self.ip + "/eportal/InterFace.do?method=login",
                          data=data, headers=self.head, cookies=self.cookie_JSESS)
        if r.status_code == 200:
            if json.loads(r.text)['result'] == "success":
                print("登录成功")
                self.userIndex = json.loads(r.text)['userIndex']
            else:
                print("登录失败:失败原因" + json.loads(r.text)['message'])

    # 登录方式有不加密和加密方式，这里直接选择不加密提交账号数据
    # def Getpageinfo(self):
    #     # RSA模数和指数获取
    #     try:
    #         head = {
    #             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    #         r = requests.post(
    #             self.ip + '/eportal/InterFace.do?method=pageInfo', data="queryString=" + self.deviceidencode,
    #             headers=head)
    #     except:
    #         print("获取秘钥信息异常")
    #     else:
    #         if r.status_code == 200:
    #             print("获取秘钥成功")
    #             # 解析json
    #             data = json.loads(r.text)
    #             self.publicKeyExponent = data['publicKeyExponent']
    #             self.publicKeyModulus = data['publicKeyModulus']
    #             self.passwordEncrypt = data['passwordEncrypt']
    #             if self.passwordEncrypt == 'true':
    #                 print("需要加密，待写")
    #                 return
    #             # print(data)

    def Getdevicedata(self):
        r = requests.get('http://www.baidu.com')
        str_pat = re.compile(r'\'(.*)\'')
        if r.text.find("baidu") != -1:
            return True
        else:
            # 解析URL中的设备数据
            self.deviceid = parse.urlparse(str_pat.findall(r.text)[0]).query
            self.ip = parse.urlparse(str_pat.findall(r.text)[0]).netloc
            self.url = str_pat.findall(r.text)[0]
            self.deviceidencode = self.deviceid.encode()
            self.cookie_JSESS = requests.get(self.url).cookies
            return False

    def AddMAC(self):
        self.cookie_JSESS['EPORTAL_COOKIE_SERVER_NAME'] = "%E8%AF%B7%E9%80%89%E6%8B%A9%E6%9C%8D%E5%8A%A1"
        self.cookie_JSESS['EPORTAL_USER_GROUP'] = "%E5%AD%A6%E7%94%9F%E7%94%A8%E6%88%B7%E7%BB%84"

        data = {"userIndex": self.userIndex,
                "mac": ""}
        r = requests.post("http://" + self.ip + "/eportal/InterFace.do?method=registerMac",
                          data=data, headers=self.head, cookies=self.cookie_JSESS)
        if r.status_code == 200:
            print(json.loads(r.text)['message'])


def main():
    net = netword("上网账号", "上网密码")
    if net.Getdevicedata() == False:
        net.Login() #登录账号
        net.AddMAC() #将当前设备MAC地址添加到无感登录
    else:
        print("已联网")


if __name__ == '__main__':
    main()

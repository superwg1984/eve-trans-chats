import time
import subprocess
import select
import requests
import os
from pathlib import Path
from googletrans import Translator
translator = Translator(service_urls=[
    'translate.google.com'
])
basePath = 'd:\Documents\EVE\logs\Chatlogs'
def follow(file):
    print(f"读取: {file}")
    """
    实现 tail －f
    """
    with open(file, 'rb') as fd:
        pos = fd.seek(0, 2)  # 打开文件时大小
        try:
            while True:
                curr_pos = fd.seek(0, 2)
                # print(f'pos: {pos}, curr_pos: {curr_pos}')
                if pos > curr_pos:  # 表示文件数据减少或清空
                    pos = fd.seek(0, 2)
                    # time.sleep(0.3)
                    continue

                line = fd.readline()
                if line:
                    ll = line.decode('utf-16', errors='ignore')
                    tmp_ll=ll.split(">")
                    name = tmp_ll[0]
                    msg = tmp_ll[1]
                    print(f"{name} --> msg:{msg}")
                    print(f"-----翻译:{translate(msg)}")
                # time.sleep(0.1)
        except KeyboardInterrupt as e:
            pass

def getFile(pd):

    p = Path(basePath)
    ll = list(p.glob(f"{pd}*.txt"))
    for i in ll:
        t = os.path.getmtime(i)
    return ll[-1]

def getPDList():
    p = Path(basePath)
    ll = list(p.glob("*.txt"))
    pd = set()
    for i in ll:
        pp = i.stem.split("_")[0]
        pd.add(pp)
    print(pd)

def translate(content):
    if len(content) > 500:
        print("too long to translate")
        return
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    params = {
        'i': content,
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'version':'2.1',
        'doctype':'json',
        'keyfrom':'fanyi.web',
        'ue':'UTF-8',
        'action':'FY_BY_REALTIME'
    }

    resp = requests.post(url=url,data=params)
    if resp.status_code != 200:
        return None
    rr = resp.text
    data = resp.json()
    msg = data['translateResult'][0][0]['tgt']
    return msg

if __name__ == '__main__':
    print(translate("This is a pen."))
    getPDList()
    file = getFile("delve.imperium")
    # file = getFile("新手帮助")

    follow(file)
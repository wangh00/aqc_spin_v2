import re
import time
import requests


def get_init():
    while 1:
        try:
            init_url = 'https://wappass.baidu.com/cap/init'
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://wappass.baidu.com",
                "Pragma": "no-cache",
                "Referer": "https://aiqicha.baidu.com",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
            data = {
                "_": str(int(round(time.time(), 3) * 1000)),
                "refer": "https://aiqicha.baidu.com",
                "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
                "ver": "2",
                "qrsign": ""
            }
            time.sleep(1.5)
            response2 = requests.post(init_url, headers=headers, data=data)
            init_response = response2.json()
            print(init_response)
            tk, _as, ds, ls = init_response['data']['tk'], init_response['data']['as'], init_response['data']['ds'], init_response['data']['ls']
            # 请求style接口
            time.sleep(1.5)
            style_url = 'https://wappass.baidu.com/cap/style'
            style_data = {
                "_": str(int(round(time.time(), 3) * 1000)),
                "refer": "https://aiqicha.baidu.com",
                "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
                "tk": tk,
                "scene": "",
                "isios": "0",
                "type": "",
                "ver": "2"
            }
            response3 = requests.post(style_url, headers=headers, data=style_data)
            style_content = response3.json()
            print(style_content)
            return init_response, style_content,"https://aiqicha.baidu.com"
        except Exception as e:
            print(e)

if __name__ == '__main__':

    init_content, style_content, location = get_init()

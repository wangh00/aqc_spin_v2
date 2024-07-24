import re
import time
import requests


def get_ip():
    proxy_url = 'http://121.89.198.233:8005/ip?num=1&Bnkey=4194f476e&auth=true'
    while True:
        try:
            ip = requests.get(url=proxy_url).json()
            if ip:
                return ip
            else:
                return None
        except Exception as e:
            print('重新获取ip:', e)


def get_init():
    while 1:
        try:
            proxys = get_ip()
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\""
            }
            # cookies = {
            #     "BAIDUID": baiduid,
            #     "BAIDUID_BFESS": baiduid
            # }

            # 获取第一个signature
            url = "https://aiqicha.baidu.com/cbae/tr"
            params = {
                "headto": "https://aiqicha.baidu.com/s?q=%E6%97%A0%E9%94%A1%E5%B8%82%E6%9C%89%E9%91%AB%E8%B4%B8%E6%98%93%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&t=0"
            }
            response1 = requests.get(url, headers=headers, params=params, allow_redirects=False, proxies=proxys,
                                     timeout=10)
            # print(response1.headers)

            res_header = response1.headers
            get_timestamp1_signature1 = re.findall(r'timestamp=(.*)&signature=(.*)', res_header.get('Location'))[0]
            timestamp1, signature1 = get_timestamp1_signature1[0], get_timestamp1_signature1[1]
            print(timestamp1, signature1)

            init_url = 'https://wappass.baidu.com/cap/init'
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://wappass.baidu.com",
                "Pragma": "no-cache",
                "Referer": res_header.get('Location'),
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }
            data = {
                "_": str(int(round(time.time(), 3) * 1000)),
                "refer": res_header.get('Location'),
                "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
                "ver": "2",
                "qrsign": ""
            }
            time.sleep(1.5)
            response2 = requests.post(init_url, headers=headers, proxies=proxys, data=data)
            init_response = response2.json()
            print(init_response)
            tk, _as, ds, ls = init_response['data']['tk'], init_response['data']['as'], init_response['data']['ds'], init_response['data']['ls']
            # 请求style接口
            time.sleep(1.5)
            style_url = 'https://wappass.baidu.com/cap/style'
            style_data = {
                "_": str(int(round(time.time(), 3) * 1000)),
                "refer": res_header.get('Location'),
                "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
                "tk": tk,
                "scene": "",
                "isios": "0",
                "type": "",
                "ver": "2"
            }
            response3 = requests.post(style_url, headers=headers, proxies=proxys, data=style_data)
            style_content = response3.json()
            print(style_content)
            return init_response, style_content, res_header.get('Location'), proxys
        except Exception as e:
            print(e)

if __name__ == '__main__':

    init_content, style_content, location, proxy = get_init()

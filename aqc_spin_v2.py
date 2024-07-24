import json
import random
import time
import warnings
from init_style import get_init
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib
import execjs
from rotate_image_classifier_inference import *

warnings.filterwarnings("ignore")


def get_fuid():
    _str = '{"userAgent":"Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F126.0.0.0%20Safari%2F537.36","canvas":"27c6869e5cc63262093ab8e664a87406","language":"zh-CN","colorDepth":"24","deviceMemory":"8","hardwareConcurrency":"12","screenResolution":"1920%2C1080","availableScreenResolution":"1040%2C1920","timezoneOffset":"-480","timezone":"","sessionStorage":"true","localStorage":"true","indexedDb":"true","addBehavior":"false","openDatabase":"false","cpuClass":"","platform":"Win32","plugins":"undefined","webgl":"547ec9734e89849aa4b8d41b836c1f80","webglVendorAndRenderer":"Google%20Inc.%20(Intel)~ANGLE%20(Intel%2C%20Intel(R)%20UHD%20Graphics%20630%20(0x00009BC5)%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)","adBlock":"false","hasLiedLanguages":"false","hasLiedResolution":"false","hasLiedOs":"false","hasLiedBrowser":"false","touchSupport":"0%2Cfalse%2Cfalse","fonts":"33","audio":"undefined"}'
    key = 'FfdsnvsootJmvNfl'
    plaintext_bytes = _str.encode('utf-8')
    # 创建AES加密对象，使用ECB模式
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    padded_plaintext = pad(plaintext_bytes, AES.block_size)
    # 加密
    ciphertext = cipher.encrypt(padded_plaintext)
    encoded_ciphertext = base64.b64encode(ciphertext)
    # print(encoded_ciphertext.decode())
    return encoded_ciphertext.decode()


def get_new_key(_as):
    mode_dict = {
        "DZ": ["0", "1", "2", "3", "4"],
        "FB": ["A", "B", "C", "D", "E", "F", "G", "a", "b", "c", "d", "e", "f", "g"],
        "GU": 'appsapi2',
        "JQ": ["O", "P", "Q", "R", "S", "T", "o", "p", "q", "r", "s", "t"],
        "NZ": ["5", "6", "7", "8", "9"],
        "eR": ["H", "I", "J", "K", "L", "M", "N", "h", "i", "j", "k", "l", "m", "n"],
        "px": "https://wappass.baidu.com/static/touch/js/lib/fingerprint.js",
        "o": ["U", "V", "W", "X", "Y", "Z", "u", "v", "w", "x", "y", "z"],
        "q4": 2
    }
    r = _as[-1]
    data = f'{_as}appsapi2'
    with open('sha3.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    _js = execjs.compile(js_code)
    if r in mode_dict['FB']:
        mess = hashlib.md5(data.encode('utf-8')).hexdigest()
    elif r in mode_dict['eR']:
        mess = hashlib.sha1(data.encode('utf-8')).hexdigest()
    elif r in mode_dict['JQ']:
        mess = hashlib.sha256(data.encode('utf-8')).hexdigest()
    elif r in mode_dict['o']:
        mess = hashlib.sha512(data.encode('utf-8')).hexdigest()
    elif r in mode_dict['DZ']:
        mess = _js.call('get_sha3_encrypt', data, 256)
    elif r in mode_dict['NZ']:
        mess = _js.call('get_sha3_encrypt', data, 512)
    else:
        return
    return mess[0:16]


def zero_pad(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = b'\0' * padding_length
    return data + padding


def get_ac_c(angle: int) -> float:
    distance = angle / 360
    final_result = float(format(distance, '.2f'))
    return final_result


def generate_trajectory_spin(num_points):
    if num_points == 0:
        return [], []

    # 初始化时间戳和坐标
    start_time = int(time.time() * 1000)
    fx_values = []
    fy_values = []

    # 生成fx和fy值
    for i in range(num_points):
        if i == 0:
            fx = random.randint(880, 900)
        elif i < num_points // 2:
            fx = fx_values[-1] - random.randint(5, 6)
        else:
            fx = fx_values[-1] + random.randint(5, 6)

        fy = random.randint(550, 570)
        fx_values.append(fx)
        fy_values.append(fy)

    # 生成轨迹点
    trajectory = []
    for i in range(num_points):
        trajectory.append({
            "t": start_time + i * random.randint(100, 200),  # 模拟时间滑动
            "fx": fx_values[i],
            "fy": fy_values[i]
        })

    return json.dumps(trajectory)


def generate_trajectory(num_points, total_distance):
    current_time = int(time.time() * 1000)
    result = []
    if num_points == 0:
        return json.dumps(result)
    elif num_points == 1:
        fx = random.randint(828, 853) + total_distance
        result.append({"t": current_time, "fx": int(fx), "fy": random.randint(660, 680)})
    else:
        average_distance = total_distance / (num_points - 1)
        # 初始化x轴的起始值
        fx_start = random.randint(828, 853)
        fx_current = fx_start
        fy_start = random.randint(660, 665)
        for i in range(num_points):
            if i == 0:
                fx = fx_start
                fy = fy_start
            else:
                # 生成每段的距离，确保每段距离不相等
                segment_distance = average_distance + random.uniform(-average_distance * 0.2, average_distance * 0.2)
                fx_current += segment_distance
                fx = int(fx_current)
                fy = fy + random.randint(2, 5)  # 逐步递增fy
            result.append({"t": current_time, "fx": fx, "fy": fy})
            current_time += random.randint(200, 4000)  # 增加时间戳
    return json.dumps(result)


def get_mv2_num(ac_c):
    if ac_c < 0.33:
        return 3
    elif 0.33 <= ac_c < 0.66:
        return 4
    else:
        return 5


class AqcSpin:
    def __init__(self):
        self.init_content, self.style_content, self.location = get_init()
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://wappass.baidu.com",
            "Pragma": "no-cache",
            "Referer": self.location,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }

    def get_fs1(self):
        back_str = self.style_content['data']['backstr']
        angle = self.get_img_file()
        ac_c = get_ac_c(angle)
        ran2 = get_mv2_num(ac_c)
        mv2 = generate_trajectory_spin(ran2)

        ran1 = 1 if ac_c < 0.5 else 2
        distance = angle * 238 / 360
        mv1 = generate_trajectory(ran1, distance)
        _str = '{"common":{"cl":[],"mv":%s,"sc":[],"kb":[],"sb":[],"sd":[],"sm":[],"cr":{"screenTop":0,"screenLeft":0,"clientWidth":1920,"clientHeight":919,"screenWidth":1920,"screenHeight":1080,"availWidth":1920,"availHeight":1040,"outerWidth":1920,"outerHeight":1040,"scrollWidth":1920,"scrollHeight":1920},"simu":0},"backstr":"%s","captchalist":{"spin-0":{"cr":{"left":815,"top":307,"width":290,"height":280},"back":{"left":884,"top":351,"width":152,"height":152},"mv":%s,"ac_c":%s,"p":{}}}}' % (
            mv1, back_str, mv2, ac_c)
        _str = _str.replace(' ', '')
        # print('json参数长度:', len(_str))
        _as = self.init_content['data']['as']
        key = get_new_key(_as)
        plaintext_bytes = _str.encode('utf-8')
        # 创建AES加密对象，使用ECB模式
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_plaintext = zero_pad(plaintext_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        encoded_ciphertext = base64.b64encode(ciphertext)
        return encoded_ciphertext.decode()

    def get_fs2(self, fs1):
        back_str = self.style_content['data']['backstr']
        need_encrypt = '{"common_en":"%s","backstr":"%s"}' % (fs1, back_str)
        need_encrypt = need_encrypt.replace(' ', '')
        _as = self.init_content['data']['as']
        key = get_new_key(_as)
        plaintext_bytes = need_encrypt.encode('utf-8')
        # 创建AES加密对象，使用ECB模式
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        padded_plaintext = zero_pad(plaintext_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        encoded_ciphertext = base64.b64encode(ciphertext)
        return encoded_ciphertext.decode()

    def get_img_file(self):
        """
        获取旋转验证码图片
        """
        img_url = self.style_content['data']['captchalist'][0]['source']['back']['path']
        print('获取到的图片链接', img_url)
        response = requests.get(img_url, headers=self.base_headers)
        with open('img_file/demo_aqc.png', 'wb') as f:
            f.write(response.content)
        time.sleep(1.5)
        # predicted_angle= get_result('img_file/demo_aqc.png')
        results, avg_diff = get_result('img_file')
        predicted_angle = results[0]['Infer']
        return predicted_angle

    def validate_log(self):
        """
        校验验证码的接口
        """
        print('开始验证登录信息')
        f1 = self.get_fs1()
        f2 = self.get_fs2(f1)
        print('f2长度:', len(f2))
        cookies = {
            "BAIDUID": "AC636876F45B05C70F953FCF19A3C6FE:FG=1",
            "BAIDUID_BFESS": "AC636876F45B05C70F953FCF19A3C6FE:FG=1",
            "RT": "\"z=1&dm=baidu.com&si=575c59e0-2dc5-420a-b83c-2a12f90a5f28&ss=lysb00o8&sl=2&tt=52z&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&r=193ayhobd&ul=l9kv&hd=l9x4\""
        }
        url = "https://wappass.baidu.com/cap/log"
        data = {
            "_": str(int(round(time.time(), 3) * 1000)),
            "refer": self.location,
            "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
            "as": self.init_content['data']['as'],
            "scene": "",
            "tk": self.init_content['data']['tk'],
            "ver": "2",
            "cv": "submit",
            "typeid": "spin-0",
            "fuid": get_fuid(),
            "fs": f2
        }
        # print(data)
        response = requests.post(url, headers=self.base_headers, data=data, cookies=cookies)
        op = response.json()['data']['op']
        if op == 1:
            print('旋转验证码校验成功!获得返回结果:', response.json()['data']['op'])
            print(response.json())
            print(response)
        else:
            print('图片验证失败,op:', op)
            tk = self.init_content['data']['tk']
            back_str = self.style_content['data']['backstr']
            data = {
                "_": str(int(round(time.time(), 3) * 1000)),
                "refer": self.location,
                "ak": "uvErNgFVAw2s19CYSdl6FLj1U3ACoUjB",
                "tk": tk,
                "scene": "",
                "isios": "0",
                "type": "spin",
                "refresh": '{"capId":"spin-0","backstr":"%s"}' % back_str,
                "ver": "2"
            }
            response_refresh = requests.post('https://wappass.baidu.com/cap/style', headers=self.base_headers,
                                             data=data)
            self.style_content = response_refresh.json()
            self.validate_log()


if __name__ == '__main__':
    aqc = AqcSpin()
    aqc.validate_log()

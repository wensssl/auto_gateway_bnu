import ctypes
import hashlib
import hmac
import json as js
import re
import time


def error(code, error, msg):
    # 构造错误信息
    if str(code).isdigit() or code == "":
        if msg is not None and msg != "":
            return msg
            # Format Error
        return error
        # Format Error
    if code == "E2901":
        return msg

    return code


def get_time():
    # 获取时间戳
    return str(int(time.time() * 1000))


def json_without_space(d):
    # 获取不含多余空格的json字符串
    pattern = r"[ ]{1}\""
    repl = '"'
    return re.sub(pattern, repl, js.dumps(d))


def md5(d, k):
    # 获取hmac-md5加密结果
    hmacmd5 = hmac.new(
        msg=d.encode("utf-8"), key=k.encode("utf-8"), digestmod=hashlib.md5
    )
    return hmacmd5.hexdigest()


def sha1(d):
    # 获取sha1加密结果
    sha1 = hashlib.sha1(d.encode("utf-8"))
    return sha1.hexdigest()


def get_response_dict(response):
    # 将response字符串转化为字典
    pattern = r"[(](.*)[)]"
    print(js.loads(re.findall(pattern, response)[0]))
    return js.loads(re.findall(pattern, response)[0])


def unsigned_right_shift(num, i):
    # 无符号右位移
    def int_overflow(num):
        # int溢出
        max_int = 2147483647
        if not -max_int - 1 <= num <= max_int:
            num = (num + (max_int + 1)) % (2 * (max_int + 1)) - max_int - 1
        return num
    if num < 0:
        return ctypes.c_uint32(num).value
    if i < 0:
        return -int_overflow(num << abs(i))
    return int_overflow(num >> i)

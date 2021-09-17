"""自动上线"""
import requests
from bs4 import BeautifulSoup

import tool
from NewBase64 import NewBase64
from xEncode import xEncode


def mkParams(url, username, password):
    # 从登录页面获取acid、ip
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    acid = soup.select("#ac_id")[0]["value"]
    ip = soup.select("#user_ip")[0]["value"]
    try:
        otp = soup.select("#otp")[0]["value"]
    except Exception as e:
        print(repr(e))
        otp = None
    params = {
        "username": username,
        "domain": "",
        "password": password,
        "ac_id": acid,
        "ip": ip,
        "double_stack": 0,
        "otp": otp,
    }
    return params


def info(d, k):
    # 构造url中info参数
    xencode = xEncode(d, k)
    print("{SRBX1}" + NewBase64().encode(xencode))
    return "{SRBX1}" + NewBase64().encode(xencode)


def pwd(d, k):
    # 加密password
    return tool.md5(d, k)


def chksum(d):
    # 构造url中chksum参数
    return tool.sha1(d)


def srunPortal(url, data, callback):
    # 请求登录
    response = requests.get(url + "/cgi-bin/srun_portal", params=data).text
    callback(tool.get_response_dict(response))
    return response


def getChallenge(url, data, callback):
    # 请求token
    response = requests.get(url + "/cgi-bin/get_challenge", params=data).text
    callback(tool.get_response_dict(response))
    return response


def login(url, data, callback):
    # 发出两个get请求，先发出get请求获得加密所用token，再对密码等进行加密后发出登录get请求
    enc = "s" + "run" + "_bx1"
    n = 200
    type = 1
    username = data["username"] + (data["domain"] or "")

    def challengeCallback(response):
        # token请求发出后，构造登录get请求所需参数
        if response["error"] != "ok":
            message = tool.error(
                response["ecode"], response["error"], response["error_msg"])
            return callback({"error": "fail", "message": message})
        token = response["challenge"]
        """i_str = '{"username":"' + username + \
            '","password":"'+data['password']+'","ip":"' + \
            (data['ip'] or response['client_ip']) + \
            '","acid":"'+data['ac_id']+'","enc_ver":"'+enc+'"}'"""
        i_dict = {
            "username": username,
            "password": data["password"],
            "ip": (data["ip"] or response["client_ip"]),
            "ac_id": data["ac_id"],
            "enc_ver": enc,
        }
        i_str = tool.json_without_space(i_dict)
        i = info(i_str, token)
        hmd5 = pwd(data["password"], token)
        chkstr = token + username
        chkstr += token + hmd5
        chkstr += token + data["ac_id"]
        chkstr += token + (data["ip"] or response["client_ip"])
        chkstr += token + str(n)
        chkstr += token + str(type)
        chkstr += token + str(i)
        os = {"device": "Windows NT", "platform": "Windows"}
        if data["otp"]:
            data["password"] = "{OTP}" + data["password"]
        else:
            data["password"] = "{MD5}" + hmd5

        params = {
            "callback": "jQuery1124000827543286740462_" + tool.get_time(),
            "action": "login",
            "username": username,
            "password": data["password"],
            "ac_id": data["ac_id"],
            "ip": data["ip"] or response["client_ip"],
            "chksum": chksum(chkstr),
            "info": i,
            "n": n,
            "type": type,
            "os": os["device"],
            "name": os["platform"],
            "double_stack": data["double_stack"],
            "_": tool.get_time(),
        }

        def authCallback(resp):
            # 用于登录请求发出后，返回结果
            if resp["error"] == "ok":
                ploy_msg = ""
                if resp["suc_msg"] == "ip_already_online_error":
                    return callback(
                        {"error": "error", "message": "IpAlreadyOnlineError"}
                    )
                if "ploy_msg" in resp:
                    ploy_msg = resp.ploy_msg
                    if ploy_msg.indexOf("E0000") == 0:
                        ploy_msg = ""
                return callback({"error": "ok", "message": ploy_msg})
            # Process Error Message
            message = tool.error(
                resp["ecode"], resp["error"], resp["error_msg"])
            print(resp)
            if "ploy_msg" in resp:
                message = resp["ploy_msg"]
            return callback({"error": "fail", "message": message})

        srunPortal(url, params, authCallback)

    params = {
        "callback": "jQuery1124000827543286740462_" + tool.get_time(),
        "username": username,
        "ip": (data["ip"] or ""),
        "_": tool.get_time(),
    }
    getChallenge(url, params, challengeCallback)


def loginErrorPrintCallback(data):
    # 输出登录结果反馈
    print(data["error"], data["message"])


def auto_login(username, password):
    # 自动上线
    url = "http://gw.bnu.edu.cn/"
    data = mkParams(url, username, password)
    login(url, data, loginErrorPrintCallback)


if __name__ == "__main__":
    username = ""
    password = ""
    auto_login(username, password)

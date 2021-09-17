"""自动下线"""
import math

import requests
from bs4 import BeautifulSoup

import tool


def getOnlineInfo(url):
    # 从登录后页面中获取ip、username
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    ip = soup.select("#user_ip")[0]["value"]
    username = soup.select("#username")[0]["value"]
    params = {
        "ip": ip,
        "username": username,
    }
    return params


def dmCallback(response, callback):
    # 用于发出下线请求后，返回结果
    if response == "logout_ok":
        return callback({"error": "ok", "message": ""})
    # Process Error Message
    message = tool.error(response, response, response)
    return callback({"error": "fail", "message": message})


def dmErrorPrintCallback(data):
    # 输出下线结果
    print(data["error"], data["message"])


def dm(
    base_url="http://gw.bnu.edu.cn/",
    success_para_str="srun_portal_success?ac_id=39&theme=bnu&srun_domain=",
    callback=dmCallback,
):
    # 发出下线get请求，自动下线，其中需要用sha1加密获取sign参数
    t = math.floor(int(tool.get_time()) / 1000)
    params_online = getOnlineInfo(base_url + success_para_str)
    params = {
        "ip": params_online["ip"],
        "username": params_online["username"],
        "time": t,
        "unbind": 0,
        "sign": "",
    }
    unbind = 0
    sign = tool.sha1(
        str(t) + params_online["username"] +
        params_online["ip"] + str(unbind) + str(t)
    )
    params["sign"] = sign
    response = requests.get(base_url + "/cgi-bin/rad_user_dm", params).text
    callback(response, dmErrorPrintCallback)
    return response


if __name__ == "__main__":
    dm()

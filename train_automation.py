# coding: utf-8
import time
import requests

from dingtalkchatbot.chatbot import DingtalkChatbot
from constant import (WEEBHOOK, PRIVATE_TOKEN)


gitlab_project_id = 2969
gitlab_merge_id = ""
gitlab_merge_username = ""
gitlab_merge_url = ""
check_result = ""
gitlab_private_token = PRIVATE_TOKEN
dingding_webhook = WEEBHOOK
check_user_one = ""
check_user_two = ""
mobile_one = ""
mobile_two = ""


get_merge_url = "https://git.uyunsoft.cn/api/v3/projects/{}/merge_request/{}/" \
                "merge?private_token={}".format(gitlab_project_id,
                                                gitlab_merge_id,
                                                gitlab_private_token)
close_merge_url = "https://git.uyunsoft.cn/api/v3/projects/{}/merge_request" \
                  "/{}?private_token={}".format(gitlab_project_id,
                                                gitlab_merge_id,
                                                gitlab_private_token)

sendInfoTitle = "发送工单合并结果信息!"
at_mobiles = [mobile_one, mobile_two]


def send_merge_result_message(result):
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sendInfoText = """
## **{}发起了mr通知**
审批人:&emsp;{}&emsp;{}\n
执行结果:&ensp;{}\n
[点击查看]({})&emsp;{}""".format(gitlab_merge_username, check_user_one,
                             check_user_two, result, gitlab_merge_url, get_time)
    xiaoding = DingtalkChatbot(dingding_webhook)
    xiaoding.send_markdown(title=sendInfoTitle, text=sendInfoText,
                           at_mobiles=at_mobiles)


def deal_gitlab_api():
    try:
        if check_result == "成功":
            response = requests.put(get_merge_url, verify=False)
            if response.status_code == 200:
                result = "合并成功"
            else:
                result = "合并失败请手动合并"
            send_merge_result_message(result)
        else:
            body = {"state_event": "close"}
            get_result = "审核不通过请更改后再提交"
            send_merge_result_message(get_result)
            requests.put(close_merge_url, data=body, verify=False)
    except Exception as e:
        print(e)


def main():
    deal_gitlab_api()


if __name__ == '__main__':
    main()


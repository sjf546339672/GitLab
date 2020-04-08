# coding: utf-8

import json
import requests
import time

from django.http import HttpResponse
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.views import View

from constant import (URGENT_LEVEL, MODEL_ID, DESCRIPTION, ROUTE_ID, LOOP_ID,
                      USER_ID, WEEBHOOK, BASE_URL, PRIVATE_TOKEN, WORK_ORDER_URL)


class Gitlab(object):

    def deal_gitlab_api(self, data):
        base_url = "http://git.uyunsoft.cn/api/v3/projects/{}/".format(data['object_attributes']["source_project_id"])
        get_merge_url = base_url + "merge_request/{}/merge?private_token={}".format(data['object_attributes']['id'], PRIVATE_TOKEN)
        try:
            response = requests.put(get_merge_url, verify=False)
            ding = Ding()
            if response.status_code == 200:
                result = "合并成功"
                ding.send_merge_result_message(data['user']['username'],
                                               result,
                                               data["object_attributes"]["url"])
            else:
                result = "合并失败请手动合并"
                ding.send_merge_result_message(data['user']['username'],
                                               result,
                                               data["object_attributes"]["url"])
        except Exception as e:
            print(e)

    def get_merge(self, data):
        if data["object_attributes"]["action"] == "open" or\
                        data["object_attributes"]["action"] == "reopen":
            body = {
                "title": "{}在git-{} 中提交了 Merge Request".format(
                    data['user']['username'],
                    data["object_attributes"]["target"]["name"]),
                "urgent_level": URGENT_LEVEL,
                "description": DESCRIPTION,
                "model_id": MODEL_ID,
                "email": data["object_attributes"]["last_commit"]["author"]["email"],
                "form": {
                    "title": "工单提交测试",
                    "ticketDesc": "用于提交工单的审核测试",
                    "dykb": "{}".format(data['object_attributes']['url']),
                    "projectid": "{}".format(data['object_attributes']["source_project_id"]),
                    "mergeid": "{}".format(data['object_attributes']['id']),
                    "privatetoken": "{}".format(PRIVATE_TOKEN),
                },
                "handle_rules": {
                    "route_id": ROUTE_ID,
                    "executors_groups": {
                        LOOP_ID: {
                            "user": [USER_ID],
                            "group": [],
                        },
                    },
                }
            }
            response = requests.post(url=WORK_ORDER_URL, json=body)
            response_json = response.json()
            print("response_json==========================>>>>>>", response_json)
            # target_url = "{0}/{1}".format(BASE_URL, response_json["id"])
            # print("target_url=========>>>>>>>", target_url)
            # ding = Ding()
            # ding.send_merge_message(data, target_url)
            # time.sleep(15)
            # Gitlab.deal_gitlab_api(self, data)


class Ding(object):

    def send_merge_message(self, data, target_url):
        get_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.localtime(time.time()))

        sendInfoTitle = "发送工单提交信息!"
        sendInfoText = "## **{}发起了mr通知** \n" \
                       "+ 审批人:&emsp;{}&emsp;{}\n" \
                       "+ [点击查看]({})&emsp;{}".format(
            data['user']['username'], "shijf", "shijf", target_url, get_time)

        print("sendInfoText=================>", sendInfoText)

        at_mobiles = []
        xiaoding = DingtalkChatbot(WEEBHOOK)
        xiaoding.send_markdown(title=sendInfoTitle,
                               text=sendInfoText,
                               at_mobiles=at_mobiles)

    def send_merge_result_message(self, username, result, merge_url):
        get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sendInfoTitle = "发送工单合并结果信息!"
        sendInfoText = "## **{}发起了mr通知** \n" \
                       "+ 审批人:&emsp;{}&emsp;{}\n" \ 
                       "+ 执行结果:&ensp;{}\n" \
                       "+ [点击查看]({})&emsp;{}".format(username,
                                                     "shijf", "shijf", result,
                                                     merge_url, get_time)
        at_mobiles = ['18365597692']
        xiaoding = DingtalkChatbot(WEEBHOOK)
        xiaoding.send_markdown(title=sendInfoTitle,
                               text=sendInfoText,
                               at_mobiles=at_mobiles)


class IndexView(View):

    def get(self, request):
        return HttpResponse("IndexView test")

    def post(self, request):
        try:
            content = request.body
            data = json.loads(content)
            print("data===========================>>>>", data)
            gitlab = Gitlab()
            gitlab.get_merge(data)
        except Exception as e:
            data = ''
            print(e)
        return HttpResponse('index')

# coding: utf-8

import json
import requests
import time

from django.http import HttpResponse
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.views import View

from constant import (URGENT_LEVEL, MODEL_ID, DESCRIPTION, ROUTE_ID, LOOP_ID,
                      WEEBHOOK, PRIVATE_TOKEN, WORK_ORDER_URL, BASE_URL,
                      check_user_one, check_user_two, mobile_one, mobile_two)


def send_merge_message(data, target_url):
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sendInfoTitle = "发送工单提交信息!"
    sendInfoText = "## **{}发起了mr通知** \n" \
                   "+ 发起人:&ensp;{}\n" \
                   "+ 仓库名:&ensp;{}\n" \
                   "+ 审批人:&ensp;{}&ensp;{}\n" \
                   "+ [gitlab请求详情]({})\n" \
                   "+ [devops工单详情]({})&ensp;{}".format(
        data['user']['username'],
        data["object_attributes"]["last_commit"]["author"]["name"],
        data["repository"]["name"], check_user_one, check_user_two,
        data["object_attributes"]["url"], target_url, get_time)

    at_mobiles = [mobile_one, mobile_two]
    xiaoding = DingtalkChatbot(WEEBHOOK)
    xiaoding.send_markdown(title=sendInfoTitle,
                           text=sendInfoText,
                           at_mobiles=at_mobiles)


class Gitlab(object):
    def get_merge(self, data):
        print(data)
        if data["object_attributes"]["action"] == "open" or \
                        data["object_attributes"]["action"] == "reopen":
            body = {
                "title": "{}在git-{} 中提交了 Merge Request".format(
                    data['user']['username'],
                    data["object_attributes"]["target"]["name"]),
                "urgent_level": URGENT_LEVEL,
                "description": DESCRIPTION,
                "model_id": MODEL_ID,
                "email":
                    data["object_attributes"]["last_commit"]["author"]["email"],
                "form": {
                    "title": "工单提交测试",
                    "ticketDesc": "用于提交工单的审核测试",
                    "url": "{}".format(data['object_attributes']['url']),
                    "projectid": "{}".format(data['object_attributes']
                                             ["source_project_id"]),
                    "mergeid": "{}".format(data['object_attributes']['id']),
                    "privatetoken": PRIVATE_TOKEN,
                    "webhook": WEEBHOOK,
                    "username": data['user']['username'],
                },
                "handle_rules": {
                    "route_id": ROUTE_ID,
                    "executors_groups": {
                        LOOP_ID: {
                            "user": [],
                            "group": [],
                        },
                    },
                }
            }
            try:
                response = requests.post(url=WORK_ORDER_URL, json=body)
                response_json = response.json()
                target_url = "{}/{}".format(BASE_URL, response_json["id"])
                send_merge_message(data, target_url)
            except Exception as e:
                print(e)


class IndexView(View):

    def get(self, request):
        return HttpResponse("IndexView test")

    def post(self, request):
        try:
            content = request.body
            data = json.loads(content)
            gitlab = Gitlab()
            gitlab.get_merge(data)
        except Exception as e:
            data = ''
            print(e)
        return HttpResponse('index')
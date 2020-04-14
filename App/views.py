# coding: utf-8

import json
import requests
import time

from django.http import HttpResponse
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.views import View

from constant import (URGENT_LEVEL, MODEL_ID, DESCRIPTION, ROUTE_ID, LOOP_ID,
                      USER_ID, WEEBHOOK, PRIVATE_TOKEN, API_KEY_ONE,
                      API_KEY_TWO, WORK_ORDER_URL, TENANT_URL, BASE_URL)


def send_merge_message(data, target_url):
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sendInfoTitle = "发送工单提交信息!"
    sendInfoText = "## **{}发起了mr通知** \n" \
                   "+ 审批人:&ensp;{}&ensp;{}\n" \
                   "+ [点击查看]({})&ensp;{}".format(
        data['user']['username'], check_user_one, check_user_two,
        target_url, get_time)

    at_mobiles = [mobile_one, mobile_two]
    xiaoding = DingtalkChatbot(WEEBHOOK)
    xiaoding.send_markdown(title=sendInfoTitle,
                           text=sendInfoText,
                           at_mobiles=at_mobiles)


class Tenate(object):
    def get_tenant_message(self, user_apikey):
        tenant_url = TENANT_URL+user_apikey
        response = requests.get(tenant_url)
        get_name = response.json()['realname']
        get_mobile = response.json()['mobile']
        return get_name, get_mobile


tenant = Tenate()
result_one = tenant.get_tenant_message(API_KEY_ONE)
result_two = tenant.get_tenant_message(API_KEY_TWO)
check_user_one = result_one[0]
# mobile_one = result_one[1]
mobile_one = "18365597692"
check_user_two = result_two[0]
# mobile_two = result_two[0]
mobile_two = "18365597692"


class Gitlab(object):
    def get_merge(self, data):
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
                    "checkuserone": result_one[0],
                    # "mobileone": result_one[1],
                    "checkusertwo": result_two[0],
                    # "mobiletwo": result_two[1],
                    "mobileone": "18365597692",
                    "mobiletwo": "18365597692",

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




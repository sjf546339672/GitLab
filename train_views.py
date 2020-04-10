# coding: utf-8

import json
import requests
import time

from django.http import HttpResponse
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.views import View

from constant import (URGENT_LEVEL, MODEL_ID, DESCRIPTION, ROUTE_ID, LOOP_ID,
                      USER_ID, WEEBHOOK, PRIVATE_TOKEN, API_KEY_ONE, BASE_URL,
                      API_KEY_TWO, WORK_ORDER_URL, TENANT_URL)


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
mobile_one = result_one[1]
check_user_two = result_two[0]
mobile_two = result_two[0]


class Gitlab(object):

    def deal_gitlab_api(self, data):
        check_result = "成功"
        base_url = "https://git.uyunsoft.cn/api/v3/projects/{}/".format(data['object_attributes']["source_project_id"])
        get_merge_url = base_url + "merge_request/{}/merge?private_token={}".format(data['object_attributes']['id'], PRIVATE_TOKEN)
        ding = Ding()
        try:
            if check_result == "成功":
                time.sleep(10)
                response = requests.put(get_merge_url, verify=False)
                if response.status_code == 200:
                    result = "合并成功"
                else:
                    result = "合并失败请手动合并"
                ding.send_merge_result_message(data['user']['username'], result, data["object_attributes"]["url"])
            else:
                close_merge_url = base_url + "merge_request/{}?private_token={}".format(data['object_attributes']['id'], PRIVATE_TOKEN)
                body = {"state_event": "close"}
                get_reult = "审核不通过请更改后再提交"
                ding.send_merge_result_message(data['user']['username'], get_reult, data["object_attributes"]["url"])
                requests.put(close_merge_url, data=body, verify=False)
        except Exception as e:
            print(e)

    def get_merge(self, data):
        if data["object_attributes"]["action"] == "open" or data["object_attributes"]["action"] == "reopen":
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
                    "mobileone": result_one[1],
                    "checkusertwo": result_two[0],
                    "mobiletwo": result_two[1],
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
            print("response_json==================>>>>>", response_json)
            print("response_json==================>>>>>")
            target_url = "{0}/{1}".format(BASE_URL, response_json["id"])
            ding = Ding()
            ding.send_merge_message(data, target_url)
            time.sleep(15)
            Gitlab.deal_gitlab_api(self, data)


class Ding(object):

    def send_merge_message(self, data, target_url):
        get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sendInfoTitle = "发送工单提交信息!"
        sendInfoText = "## **{}发起了mr通知** \n" \
                       "+ 审批人:&emsp;{}&emsp;{}\n" \
                       "+ [点击查看]({})&emsp;{}".format(
            data['user']['username'], check_user_one, check_user_two, target_url, get_time)

        at_mobiles = [mobile_one, mobile_two]
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
                                                     check_user_one, check_user_two, result,
                                                     merge_url, get_time)
        at_mobiles = [mobile_one, mobile_two]
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
            print("data==================", data)
            gitlab = Gitlab()
            gitlab.get_merge(data)
        except Exception as e:
            data = ''
            print(e)
        return HttpResponse('index')



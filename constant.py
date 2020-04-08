# coding: utf-8

CALL_BACK = ""  # 回调函数可以不填写
API_KEY = "615d874bd54a4d10a00001a3b282a4c4"  # apikey值必填
URGENT_LEVEL = 1  # 工单等级1-5（1等级最低）
MODEL_ID = "a0dd3b4ed2764a3e8c8365c14873ed9e"  # 模型id
DESCRIPTION = "用于提交工单的审核测试"  # 工单描述信息
ROUTE_ID = "7ffc00812f9c43718aefc7818d6e8420"  # 对应环节id/线id
LOOP_ID = "f61b1f29047b4e22bd1734708e74f40a"  # 环节id
USER_ID = "372f9afa0aea4a748f2183a628b74b2a"  # 用户id
BASE_URL = "http://devops.uyunsoft.cn/itsm/#/ticket/detail"
PRIVATE_TOKEN = "xVarr9xLmAv6vro18P4r"  # 查找路径gitlab->profile setting->account

WEEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=8f5677735dfcd3bff5626b334345df8e2766fcc128e713932ca3737bd609d3ec"
WORK_ORDER_URL = "http://devops.uyunsoft.cn/itsm/openapi/v3/tickets/create" \
                 "?callback={0}&apikey={1}".format(CALL_BACK, API_KEY)

"""
geturl          https://git.uyunsoft.cn/shijf/WorkOrder/merge_requests/47
projectid       2969
mergeid         22187
WEEBHOOK        https://oapi.dingtalk.com/robot/send?access_token=8f5677735dfcd3bff5626b334345df8e2766fcc128e713932ca3737bd609d3ec
PRIVATE_TOKEN   xVarr9xLmAv6vro18P4r
"""


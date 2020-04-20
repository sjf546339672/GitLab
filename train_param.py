# coding: utf-8
merge_body = {
    "title": "测试1",  # string 工单标题，必填
    "urgent_level": "3",  # integer 优先级，必填
    "description": "测试使用",  # string 描述
    "model_id": "e4e4ea895f1349cf8a3445d20d7b6924",  # string 模型id，必填
    "ticket_source": "",  # string 工单来源
    "email": "shijf@broada.com",  # string 邮箱
    "form": {
        "title": "测试2",
        "urgentLevel": "3",
        "ticketDesc": "用于测试"
    },  # 表单内容 字段code与值对应(key:value)
    "relation_cis": {
        "id": "",  # string 配置项id
        "name": "",  # string 配置项名称
        "type": "",  # string 资源类型
        "status": "",  # string 配置项状态
        "sandbox_id": "",  # string 沙箱id
        "task_id": "",  # string 沙箱任务id
        "code": "",  # string 对应的字段code
    },  # 配置项
    "handle_rules": {  # 处理路径，必填
        "route_id": "",  # string  目标环节/线id，必填，
        "depart_id": "",  # string 所在部门id
        "message": "hello world",  # string 评论内容
        "executors_groups": {
            # 工单的处理人或组
            "环节id": {  # 指定环节id
                "user": [],  # 用户id数组或组id数组 string
                "group": [],  # 用户id数组或组id数组 string
            },
        },
    }
}

request_body = {
    'object_kind': 'merge_request',
    'user': {
        'name': 'junfeng shi', 'username': 'shijf',
        'avatar_url': 'https://secure.gravatar.com/avatar/544a967d584bd358931427803a5367b2?s=80&d=identicon'
    },
    'repository': {
        'name': 'WorkOrder',
        'url': 'git@git.uyunsoft.cn:shijf/WorkOrder.git',
        'description': '测试',
        'homepage': 'https://git.uyunsoft.cn/shijf/WorkOrder'
    },
    'object_attributes': {
        'id': 21852,
        'target_branch': 'dev',
        'source_branch': 'test',
        'source_project_id': 2969,
        'author_id': 481,
        'assignee_id': None,
        'title': 'xxxx',
        'created_at': '2020-03-25 07:32:48 UTC',
        'updated_at': '2020-03-26 01:17:09 UTC',
        'milestone_id': None,
        'state': 'closed',
        'merge_status': 'can_be_merged',
        'target_project_id': 2969,
        'iid': 7,
        'description': '',
        'position': 0,
        'locked_at': None,
        'updated_by_id': None,
        'merge_error': None,
        'merge_params': {},
        'merge_when_build_succeeds': False,
        'merge_user_id': None,
        'source': {
            'name': 'WorkOrder',
            'ssh_url': 'git@git.uyunsoft.cn:shijf/WorkOrder.git',
            'http_url': 'https://git.uyunsoft.cn/shijf/WorkOrder.git',
            'web_url': 'https://git.uyunsoft.cn/shijf/WorkOrder',
            'namespace': 'shijf',
            'visibility_level': 0
        },
        'target': {
            'name': 'WorkOrder',
            'ssh_url': 'git@git.uyunsoft.cn:shijf/WorkOrder.git',
            'http_url': 'https://git.uyunsoft.cn/shijf/WorkOrder.git',
            'web_url': 'https://git.uyunsoft.cn/shijf/WorkOrder',
            'namespace': 'shijf',
            'visibility_level': 0
        },
        'last_commit': {
            'id': '54b27496ad57a763ed3c9492ccbbe3e030c5d248',
            'message': 'create branch\n',
            'timestamp': '2020-03-25T15:07:53+08:00',
            'url': 'https://git.uyunsoft.cn/shijf/WorkOrder/commit/54b27496ad57a763ed3c9492ccbbe3e030c5d248',
            'author': {
                'name': 'sjf',
                'email': '546339672@qq.com'
            }
        },
        'work_in_progress': False,
        'url': 'https://git.uyunsoft.cn/shijf/WorkOrder/merge_requests/7',
        'action': 'close'
    }
}
print(request_body["object_attributes"]["last_commit"]["author"]["name"])

response_json = {
    'id': '7bdf6397b3994c879fe61577adf8a285',
    'title': 'shijf在git-WorkOrder 中提交了 Merge Request',
    'flowNo': 'ARSR20032600016',
    'ticketDesc': '用于提交工单的审核测试',
    'urgentLevel': 1,
    'createTime': 1585193180025,
    'ticketSource': 'web',
    'modelId': 'a0dd3b4ed2764a3e8c8365c14873ed9e'
}

url1 = "http://devops.uyunsoft.cn/portal/#/itsm/ticket/detail/" \
       "b40a9b05fdb64c2c9fa61921d2abd5d0?" \
       "tacheNo=2&" \
       "tacheType=0&" \
       "tacheId=f61b1f29047b4e22bd1734708e74f40a&" \
       "modelId=a0dd3b4ed2764a3e8c8365c14873ed9e&" \
       "caseId=bbeba725c3db428c85ea976ac67ab199"

MODEL_ID = "a0dd3b4ed2764a3e8c8365c14873ed9e"
LOOP_ID = "f61b1f29047b4e22bd1734708e74f40a"
base_url = "http://devops.uyunsoft.cn/portal/#/itsm/ticket/detail"
a = "{0}/{1}".format(base_url, response_json["id"])

order_message = {
    "ticket_id": "",  # string (uuid(32)) 工单id
    "model_id": "",  # string (uuid(32)) 模型id
    "handle_type": "",  # integer 工单处理类型，0：接单 1：提交工单 2：关闭工单 3：废除工单 4：回退工单 5：取回工单
    "activity_id": "",  # string (uuid(32)) 当前环节id
    "form": {},  # 表单内容 字段code与值对应
    "title": "",  # string工单标题
    "urgent_level": "",  # integer优先级
    "description": "",  # string工单描述
    "ticket_source": "",  # string工单来源
    "parallelism_tache_user": {
        # 并行环节时需额外指定，并行用户列表 如{"activityId":["userId1","userId2"]}
        "并行环节id": []  # 用户id数组string用户ID
    },
    "parallelism_tache_group": {
        # 并行环节时需额外指定，并行用户组列表 如{"activityId":["groupId1","groupId2"]}
        "并行环节id": []  # 用户组id数组string用户ID
    },
    "handle_rules": {
        # 处理路径必填
        "route_id": "",  # string目标环节/线id，必填，对于敏捷模型来说，如果下一环
        # 节是并行环节，则可以不传。对于高级模型来说，如果下一环节是并行网关，则传对应提交到并行网关的流程线ID
        "depart_id": "",  # string所在部门id
        "message": "",  # string评论内容
        "executors_groups": {
            # 工单的处理人或组
            "环节id": {
                # 指定环节id
                "user": [],  # 用户id数组或组id数组 string
                "group": [],  # 用户id数组或组id数组 string
            },
        },
    }

}

order = {
    "ticket_id": "185c122a2cb74a9bb3b1c887965e6da1",
    "model_id": "a0dd3b4ed2764a3e8c8365c14873ed9e",
    "handle_type": 1,
    "activity_id": "f61b1f29047b4e22bd1734708e74f40a",
    "form": {},
    "title": "shijf在git-WorkOrder 中提交了 Merge Request",
    "urgent_level": 1,
    "description": "用于提交工单的审核测试",
    "parallelism_tache_user": {"": [""]},
    "parallelism_tache_group": {"": []},
    "handle_rules": {
        "route_id": "7ffc00812f9c43718aefc7818d6e8420",
        "executors_groups": {
            "f61b1f29047b4e22bd1734708e74f40a": {
                "user": ["372f9afa0aea4a748f2183a628b74b2a"],
                "group": [],
            },
        },
    }

}

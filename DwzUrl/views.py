# coding: utf-8

import django
import os
import xxhash

from django.shortcuts import redirect
from DwzUrl.models import ShortURLModel

os.environ.setdefault('DJANGO_SETTING_MODULE', 'GitLab.settings')
django.setup()


class DealUrl(object):

    def get_hash(self, text):
        digest_tool = xxhash.xxh64()
        digest_tool.reset()
        digest_tool.update(text)
        result = digest_tool.intdigest()
        return result

    def encode(self, num):
        alphabet = "23456789abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ"
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            num, rem = divmod(num, base)
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    def convert_short_url(self, url):
        """生成短链接"""
        hash_code = self.get_hash(url)
        url_code = self.encode(hash_code)
        return url_code

    def deal_url(self, url):

        url_code = self.convert_short_url(url)
        try:
            shortmodel = ShortURLModel()
            get_url_code_count = ShortURLModel.objects.filter(short_url=url_code).count()
            if get_url_code_count == 0:
                shortmodel.long_url = url
                shortmodel.short_url = url_code
                shortmodel.save()
            else:
                print("数据已存在无需重复添加")
            short_url = "http://10.1.240.102:9003/dwz/" + url_code
            return short_url, url_code
        except Exception as e:
            print(e)

    def verify_url_code(self, url_code):
        res = ShortURLModel.objects.filter(short_url=url_code).first()
        try:
            if res:
                response = redirect(res.long_url)
            else:
                response = "数据不存在"
            return response
        except Exception as e:
            print(e)


def dwz(request, url_code):
    dealurl = DealUrl()
    response = dealurl.verify_url_code(url_code)
    return response




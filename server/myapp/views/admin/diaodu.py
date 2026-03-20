# Create your views here.
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Baoxiu  # 新增导入
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import BaoxiuSerializer# 假设你已经创建了对应的序列化器

import requests
import json

API_KEY = "catAqER2T1shJdOPRd9S00SX"
SECRET_KEY = "mfgdlwQhqIO92DEyKzgYJHYGEuVOw37A"


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


@api_view(['POST'])
def list_api(request):
    if request.method == 'POST':
        url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers?access_token=" + get_access_token()
        # 使用原始请求数据作为payload
        payload = json.dumps({
            "group_id": "group_jingju"
        }, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        # 直接返回百度API的原始响应数据
        data=response.json()['result']
        return APIResponse(code=0, msg='查询成功', data=data)
@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if request.method == 'POST':
        url="https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=" + get_access_token()
        params = {
            "group_id": "group_jingju",
            "user_id": request.data["id"],
            "image":request.data["img"][23:],
            "image_type": "BASE64",
        }
        print(params)
        payload = json.dumps(params, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        print(response.text)
        return APIResponse(code=0, msg='新增成功')




@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if request.method == 'POST':
        url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/delete?access_token=" + get_access_token()
        # 使用原始请求数据作为payload
        payload = json.dumps({
            "group_id": "group_jingju",
        "user_id": request.data["ids"]
        }, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        # 直接返回百度API的原始响应数据
        data = response.json()['result']
        return APIResponse(code=0, msg='删除成功', data=data)



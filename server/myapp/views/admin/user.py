# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes
import json
from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import User
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import UserSerializer, LoginLogSerializer
from myapp.utils import md5value
import requests
import  myapp.views.admin.airline as airline

def make_login_log(request):
    try:
        username = request.data['username']
        data = {
            "username": username,
            "ip": utils.get_ip(request),
            "ua": utils.get_ua(request)
        }
        serializer = LoginLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    except Exception as e:
        print(e)






API_KEY = "catAqER2T1shJdOPRd9S00SX"
SECRET_KEY = "mfgdlwQhqIO92DEyKzgYJHYGEuVOw37A"
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
@api_view(['POST'])
def admin_login(request):
    username = request.data['username']

    if "admin" not in username:
        people = []
        airlines = airline.Airline.objects.filter(id__contains="")
        airerializer = airline.AirlineSerializer(airlines, many=True)
        for i in airerializer.data:
            people+=eval(i['people'])

        if username not in people:
            return APIResponse(code=1, msg='您此刻暂无权限登录，请联系管理员')




        password = request.data['password']
        url = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + get_access_token()
        # 使用原始请求数据作为payload
        payload = json.dumps({
            "group_id_list": "group_jingju",
            "image": password[23:],
            "image_type": "BASE64",
            "user_id": username
        }, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        data1 = response.json()
        print(data1, data1["error_msg"])
        if data1["error_msg"]!='SUCCESS':
            if data1["error_msg"]=='match user is not found':
                return APIResponse(code=1, msg='该工号尚未录入人脸，请尽快联系管理员录入')
            return APIResponse(code=1, msg='人脸识别失败，原因：'+data1["error_msg"]+',请联系管理员')
        elif data1["result"]["user_list"][0]["score"]<70:
            return APIResponse(code=1, msg='人脸与工号不符，有疑问请联系管理员')
        data = {
            'username': username,
            'password': 1,
            'admin_token': md5value(username)  # 生成令牌
        }
        user=User()
        user.username = username
        user.password = 1
        user.admin_token = md5value(username)

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            make_login_log(request)
            return APIResponse(code=0, msg='登录成功', data=serializer.data)
        else:
            print(serializer.errors)
    else:
        password = utils.md5value(request.data['password'])
        users = User.objects.filter(username=username, password=password, role__in=['1','3'])
        if len(users) > 0:
            user = users[0]
            if user.status != '0':
                return APIResponse(code=1, msg='用户已停用')
            data = {
                'username': username,
                'password': password,
                'admin_token': md5value(username)  # 生成令牌
            }
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                #serializer.save()
                #make_login_log(request)
                return APIResponse(code=0, msg='登录成功', data=serializer.data)
            else:
                print(serializer.errors)

    return APIResponse(code=1, msg='用户名或密码错误')


@api_view(['GET'])
def info(request):
    if request.method == 'GET':
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        users = User.objects.filter(role__isnull=False).order_by('-create_time')
        serializer = UserSerializer(users, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
def register(request):

    print(request.data)
    if not request.data.get('username', None) or not request.data.get('password', None):
        return APIResponse(code=1, msg='用户名或密码不能为空')
    users = User.objects.filter(username=request.data['username'])
    if len(users) > 0:
        return APIResponse(code=1, msg='该用户名已存在')

    data = request.data.copy()
    data.update({'password': utils.md5value(request.data['password'])})
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='注册成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='注册失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    print(request.data)
    if not request.data.get('username', None) or not request.data.get('password', None):
        return APIResponse(code=1, msg='用户名或密码不能为空')
    users = User.objects.filter(username=request.data['username'])
    if len(users) > 0:
        return APIResponse(code=1, msg='该用户名已存在')

    data = request.data.copy()
    data.update({'password': utils.md5value(request.data['password'])})
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    data = request.data.copy()
    if request.data['password'] != user.password:
     data.update({'password': utils.md5value(request.data['password'])})
    if 'username' in data.keys():
        del data['username']
    serializer = UserSerializer(user, data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def updatePwd(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    password = request.data.get('password', None)
    newPassword1 = request.data.get('newPassword1', None)
    newPassword2 = request.data.get('newPassword2', None)

    if not password or not newPassword1 or not newPassword2:
        return APIResponse(code=1, msg='不能为空')

    if user.password != utils.md5value(password):
        return APIResponse(code=1, msg='原密码不正确')

    if newPassword1 != newPassword2:
        return APIResponse(code=1, msg='两次密码不一致')

    data = request.data.copy()
    data.update({'password': utils.md5value(newPassword1)})
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        User.objects.filter(id__in=ids_arr).delete()
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')


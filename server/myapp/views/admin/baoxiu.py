# Create your views here.
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Baoxiu  # 新增导入
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import BaoxiuSerializer# 假设你已经创建了对应的序列化器




@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        baoxius = Baoxiu.objects.filter().order_by('-bianhao') # 修改为查询Baoxiu
        serializer = BaoxiuSerializer(baoxius, many=True)  # 使用BaoxiuSerializer
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = BaoxiuSerializer(data=request.data)  # 使用BaoxiuSerializer
    print(serializer.is_valid())

    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    return APIResponse(code=1, msg=serializer.errors)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        baoxiu = Baoxiu.objects.get(pk=pk)  # 修改为查询Baoxiu
    except Baoxiu.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = BaoxiuSerializer(baoxiu, data=request.data)  # 使用BaoxiuSerializer
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg=serializer.errors)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Baoxiu.objects.filter(Q(bianhao__in=ids_arr)).delete()  # 修改为删除Baoxiu
    except Baoxiu.DoesNotExist:

        return APIResponse(code=1, msg='对象不存在')
    except Exception as e:
        print(e)
    return APIResponse(code=0, msg='删除成功')

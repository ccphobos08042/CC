# Create your views here.
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Jingjucabinet  # 新增导入
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import JingjuCabinetSerializer  #




@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        jingjucabinets = Jingjucabinet.objects.filter(location__contains=keyword)  # 修改为查询Jingjucabinet
        serializer = JingjuCabinetSerializer(jingjucabinets, many=True)  # 使用JingjuCabinetSerializer
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = JingjuCabinetSerializer(data=request.data)  # 使用JingjuCabinetSerializer
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    return APIResponse(code=1, msg='创建失败')

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        jingjucabinet = Jingjucabinet.objects.get(pk=pk)  # 修改为查询Jingjucabinet
    except Jingjucabinet.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = JingjuCabinetSerializer(jingjucabinet, data=request.data)  # 使用JingjuCabinetSerializer
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败')

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Jingjucabinet.objects.filter(Q(id__in=ids_arr)).delete()  # 修改为删除Jingjucabinet
    except Jingjucabinet.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    except Exception as e:
        print(e)
    return APIResponse(code=0, msg='删除成功')

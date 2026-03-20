# Create your views here.
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from PIL import Image
import torchvision.transforms as transforms
from ultralytics import YOLO
import base64
from io import BytesIO
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Returnjingju  # 新增导入
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ReturnjingjuSerializer
import os
import base64
from django.core.files.base import ContentFile
import serial


# ... existing code ...


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        people =request.GET.get("people", '')
        if people=="admin":
            ReturnJingjus = Returnjingju.objects.filter(

            )
        else:ReturnJingjus = Returnjingju.objects.filter(returntime="")  # 修改为查询ReturnJingju
        serializer = ReturnjingjuSerializer(ReturnJingjus, many=True)  # 使用ReturnJingjuSerializer

        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    serializer = ReturnjingjuSerializer(data=request.data)  # 使用ReturnJingjuSerializer

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
        returnjingju = Returnjingju.objects.get(pk=pk)  # 修改为查询Jingjucabinet
    except Returnjingju.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = ReturnjingjuSerializer(returnjingju, data=request.data)  # 使用JingjuCabinetSerializer
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败')

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    print(request)
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')

        ids_arr = ids.split(',')
        ReturnJingju.objects.filter(Q(id__in=ids_arr)).delete()  # 修改为删除ReturnJingju
    except RetuenJingju.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    except Exception as e:
        print(e)
    return APIResponse(code=0, msg='删除成功')

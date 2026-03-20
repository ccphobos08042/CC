# Create your views here.
import json
from datetime import datetime, timedelta
from myapp.models import Airline
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from PIL import Image
import torchvision.transforms as transforms
from ultralytics import YOLO
import base64
from io import BytesIO
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Jingju  # 新增导入
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import JingjuSerializer
import os
import base64
from django.core.files.base import ContentFile
import serial
from myapp.models import Jingjucabinet
from myapp.serializers import JingjuCabinetSerializer
from myapp.models import Returnjingju
from myapp.serializers import ReturnjingjuSerializer

@api_view(['POST'])
def opendoor(request):
    if request.method == 'POST':
        return APIResponse(code=0, msg='串口打开成功')
    '''
        try:
            PORT = "COM8"
            BAUDRATE = 9600
            BYTESIZE = serial.EIGHTBITS
            PARITY = serial.PARITY_NONE
            STOPBITS = serial.STOPBITS_ONE
            UNLOCK_CMD = bytes.fromhex("8A0101119B")
            #开锁命令 
            8A(开锁命令头)01(板地址)01(锁地址)11(开锁指令)9B(异或校验)
              
            ser = serial.Serial(
                port=PORT,
                baudrate=BAUDRATE,
                bytesize=BYTESIZE,
                parity=PARITY,
                stopbits=STOPBITS,
                timeout=1)
            ser.write(UNLOCK_CMD)
            if 'ser' in locals():
                ser.close()
            #return APIResponse(code=0, msg='串口打开成功')
        except Exception as e:
            print(e)
            return APIResponse(code=1, msg='串口打开失败')
            '''

        # 发送指令


@api_view(['POST'])
def yolov8(request):
    a = {"BS": "匕首",
         "SSG": "伸缩棍",
         "JCJ": "检查镜",
         "QGSD": "强光手电",
         "FGST": "防割手套",
         "FGBX": "反光背心",
         "SK": "手铐",
         "BST": "匕首套",
         "YSS": "约束绳",
         "ZQYG": "执勤腰包",
         "ZD": "扎带",
         "MHT": "灭火毯",
         "FCBX": "防刺背心",
         }
    if request.method == 'POST':
        try:
            # 获取base64图片数据
            image_data = request.data.get('image', '')
            if not image_data:
                return APIResponse(code=1, msg='图片数据为空')
            model = YOLO('C:\\Users\\10642\\Desktop\\th_model\\weights\\best.pt')
            #model = YOLO('C:\\Users\\10642\\Desktop\\weights\\yolov8s.pt')
            model.eval()
            # 解码base64
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            image = Image.open(data)
            transform = transforms.Compose([
                transforms.Resize((640, 640)),  # YOLO通常使用640x640输入
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet标准化
            ])
            input_tensor = transform(image).unsqueeze(0)
            results = model.predict(image)
            for result in results:
                plotted_image = result.plot()
                plotted_image = Image.fromarray(plotted_image)
                # 将图片保存到内存缓冲区
                buffered = BytesIO()
                plotted_image.save(buffered, format="JPEG", quality=95)
                # 转换为base64字符串
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                #print(img_str)
                boxes = result.boxes  # 获取边界框信息
                dictdate = {
                }
                for box in boxes:
                    cls = model.names[int(box.cls)]  # 类别ID

                    if cls in a:
                        dictdate[a[cls]] = 1
                    else:
                        dictdate[cls] = 1
                datedate = {
                    "img": img_str,
                    "data": dictdate
                }
            return APIResponse(code=0, msg='检测成功', data=datedate)


        except Exception as e:
            print(e)
            return APIResponse(code=1, msg='检测失败')


# ... existing code ...


@api_view(['GET'])
def list_api(request):

    if request.method == 'GET':
        keyword = request.GET.get("id", '')
        people = request.GET.get("people", '')
        if people !="":
            airlines = Airline.objects.filter()
            for airline in airlines:
                if people in airline.people:
                    time1=datetime.strptime(airline.begin_time, "%Y-%m-%d %H:%M")
                    time_diff =time1.replace(tzinfo=None) - datetime.now()
                    if timedelta(hours=0) < time_diff :
                        location=(airline.begin_ariport)
                    else:
                        location=(airline.end_ariport)

            jingjucabinets = Jingjucabinet.objects.filter()
            for jingjucabinet in jingjucabinets:
                if location in jingjucabinet.location:#若位置存在警具柜
                    x=0
                    if jingjucabinet.quantity>x:
                        x=jingjucabinet.quantity
                        y=jingjucabinet.id
            jingjus = Jingju.objects.filter(cabinet=y, status=2)
            serializer = JingjuSerializer(jingjus, many=True)  # 使用JingjuSerializer
            returnjingjus=Returnjingju.objects.filter(people=people)
            for i in returnjingjus:

                if i.returntime=="":
                    return APIResponse(code=1, msg="无可借")
            return APIResponse(code=0, msg='查询成功', data=serializer.data)

        if keyword != '':
            jingjus = Jingju.objects.filter(id=keyword)  # 修改为查询Jingju
            serializer = JingjuSerializer(jingjus, many=True)  # 使用JingjuSerializer
            return APIResponse(code=0, msg='查询成功', data=serializer.data)
        jingjus = Jingju.objects.filter()  # 修改为查询Jingju
        serializer = JingjuSerializer(jingjus, many=True)  # 使用JingjuSerializer
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = JingjuSerializer(data=request.data)  # 使用JingjuSerializer
    #print(serializer)
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
        jingju = Jingju.objects.get(pk=pk)  # 修改为查询Jingju
    except Jingju.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    print(request.data)
    data1=jingju.item
    for i in request.data:
        if "item[" in i:
            data1[i[5:-1]]=eval(request.data[i])
            data2={"id":pk,"item":data1}
            print(data2)
            serializer = JingjuSerializer(jingju, data=data2)  # 使用JingjuSerializer
            if serializer.is_valid():
                serializer.save()
                return APIResponse(code=0, msg='更新成功', data=serializer.data)

    serializer = JingjuSerializer(jingju, data=request.data)  # 使用JingjuSerializer
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败'+str(serializer.errors))


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    print(request)
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')

        ids_arr = ids.split(',')
        Jingju.objects.filter(Q(id__in=ids_arr)).delete()  # 修改为删除Jingju
    except Jingju.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    except Exception as e:
        print(e)
    return APIResponse(code=0, msg='删除成功')

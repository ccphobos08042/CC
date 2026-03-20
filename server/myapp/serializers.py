from rest_framework import serializers

from myapp.models import Airline,Jingju, User, LoginLog, OpLog, ErrorLog,Jingjucabinet,Baoxiu, Returnjingju










class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('password',)


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = OpLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = ErrorLog
        fields = '__all__'




class JingjuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jingju
        fields = '__all__'

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'
        extra_kwargs = {
            'people': {'required': False},  # 将status设为可选
        }
class JingjuCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jingjucabinet
        fields = '__all__'
        extra_kwargs = {
            'status': {'required': False},  # 将status设为可选
            'quantity': {'required': False}  # 将quantity设为可选
        }

class BaoxiuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baoxiu
        fields = '__all__'
class ReturnjingjuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returnjingju
        fields = '__all__'
        extra_kwargs = {
            'getcabinet': {'required': False},  # 将status设为可选
            'returncabinet': {'required': False},  # 将quantity设为可选
            'gettime': {'required': False},  # 将status设为可选
            'returntime': {'required': False},  # 将status设为可选
            'people': {'required': False},  # 将status设为可选
        }


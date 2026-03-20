from django.db import models

class Baoxiu(models.Model):
    # Auto - incrementing primary key
    bianhao = models.AutoField(primary_key=True)
    # Item name, cannot be empty
    wupin = models.CharField(max_length=50,null=True)
    # Guanhao field, can be empty
    guanhao = models.IntegerField(null=True, blank=True)
    # Baohao field, can be empty
    baohao = models.IntegerField(null=True, blank=True)
    # Repair time, default to current time
    baoxiushijian = models.DateTimeField(auto_now_add=True)
    # Repair person's name, cannot be empty
    baoxiuren = models.CharField(max_length=50,null=True)
    # Status field
    zhuangtai = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "baoxiu"

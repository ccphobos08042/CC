from django.db import models

class Returnjingju(models.Model):
    id = models.AutoField(primary_key=True)
    getcabinet = models.IntegerField()
    returncabinet = models.IntegerField()
    jingju = models.IntegerField()
    gettime = models.CharField(max_length=20)  # 格式如 '2024-03-20 14:30:00'
    returntime = models.CharField(max_length=20)
    people = models.IntegerField()

    class Meta:
        db_table = "returnjingju"
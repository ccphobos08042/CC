from django.db import models



class Jingjucabinet(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    type = models.IntegerField()
    status = models.IntegerField()
    capacity = models.IntegerField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)

    class Meta:
        db_table = "jingjucabinet"


from django.db import models
class Jingju(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    type = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    cabinet = models.IntegerField(null=True)
    item = models.JSONField(null=True)
    last_people = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "jingju"


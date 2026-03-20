from django.db import models



class Airline(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    begin_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    begin_ariport = models.CharField(max_length=255)
    end_ariport = models.CharField(max_length=255)
    people = models.JSONField()

    class Meta:
        db_table = "airline"

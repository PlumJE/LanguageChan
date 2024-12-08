from django.db import models

# Create your models here.
class LessonMap(models.Model):
    lessonmapnum = models.IntegerField(primary_key=True, default=0)
    name = models.TextField(blank=True, null=True)
    bgimg = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'LessonMap'

class BaseLesson(models.Model):
    lessonnum = models.IntegerField(primary_key=True, default=0)
    theme = models.TextField(blank=True, null=True)
    x_cor = models.FloatField(blank=True, null=True)
    y_cor = models.FloatField(blank=True, null=True)
    btnimg = models.TextField(blank=True, null=True)
    bgimg = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
    
class English(BaseLesson):
    class Meta:
        managed = True
        db_table = 'English'

class Chinese(BaseLesson):
    class Meta:
        managed = True
        db_table = 'Chinese'
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsersChara(models.Model):
    usernum = models.IntegerField(null=True)
    charanum = models.IntegerField(null=True)
    lvl = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersChara'
        unique_together = ('usernum', 'charanum')


class UsersFriends(models.Model):
    usernum = models.IntegerField(null=True)
    friendnum = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersFriends'
        unique_together = ('usernum', 'friendnum')


class UsersItem(models.Model):
    usernum = models.IntegerField(unique=True, null=True)
    money = models.IntegerField(default=100)
    jewel = models.IntegerField(default=10)

    class Meta:
        managed = True
        db_table = 'UsersItem'


class UsersProgress(models.Model):
    usernum = models.IntegerField(null=True)
    lessonmapnum = models.IntegerField(null=True)
    progress = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'UsersProgress'
        unique_together = ('usernum', 'lessonmapnum')


class UsersOption(models.Model):
    usernum = models.IntegerField(unique=True, null=True)
    birthday = models.TextField(null=True)
    language = models.TextField(default='Korean')
    
    class Meta:
        managed = True
        db_table = 'UsersOption'

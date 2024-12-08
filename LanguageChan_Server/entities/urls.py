from django.urls import path
from .views import *

urlpatterns = [
    path('charainfo/', getCharaInfo),
    path('charaatk/', getCharaAtk),
    path('charadps/', getCharaDps),
    path('enemyinfo', getEnemyInfo),
    path('get_image/', getImage),
]
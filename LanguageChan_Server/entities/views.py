from os import path
from math import log
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import *
from .models import *


# Create your views here.
@api_view(['GET'])
def getCharaInfo(request):
    try:
        charanum = request.data.get('charanum')

        chara = CharaInfo.objects.get(charanum=charanum)

        return Response(
            {
                'name': chara.name,
                'headimg': chara.headimg,
                'fullimg': chara.fullimg,
                'fightimg': chara.fightimg,
            }
        )
    except APIException as e:
        return Response(
            {'error': str(e)},
            status=e.status_code
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getCharaAtk(request):
    try:
        charanum = request.data.get('charanum')
        lvl = request.data.get('lvl')

        chara = CharaInfo.objects.get(charanum=charanum)
        atkexp = chara.atkexp

        return Response(
            {'atk': exp_calculation(atkexp, lvl)},
            status=status.HTTP_200_OK
        )
    except APIException as e:
        return Response(
            {'error': str(e)},
            status=e.status_code
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getCharaDps(request):
    try:
        charanum = request.data.get('charanum')
        lvl = request.data.get('lvl')

        chara = CharaInfo.objects.get(charanum=charanum)
        dpsexp = chara.dpsexp

        return Response(
            {'dps': exp_calculation(dpsexp, lvl)},
            status=status.HTTP_200_OK
        )
    except APIException as e:
        return Response(
            {'error': str(e)},
            status=e.status_code
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def exp_calculation(exp:str, lvl:str):
    operand = 0.0
    operator = ''
    try:
        for elmnt in exp.split(' '):
            if elmnt == 'lvl':
                elmnt = lvl
            if not elmnt.isdigit():
                operator = elmnt
            else:
                elmnt = float(elmnt)
                match operator:
                    case '+':
                        operand += elmnt
                    case '-':
                        operand -= elmnt
                    case '*':
                        operand *= elmnt
                    case '/':
                        operand /= elmnt
                    case '**':
                        operand = operand ** elmnt
                    case '//':
                        operand = log(operand, elmnt)
                    case _:
                        operand = elmnt
        return operand
    except Exception as e:
        print('expression calculation FAILED!!!!')
        raise e

@api_view(['GET'])
def getEnemyInfo(request):
    try:
        enemynum = request.data.get('enemynum')

        enemy = EnemyInfo.objects.get(enemynum=enemynum)

        return Response(
            {
                'name': enemy.name,
                'headimg': enemy.headimg,
                'fullimg': enemy.fullimg,
                'fightimg': enemy.fightimg,
                'atk': enemy.atk,
                'dps': enemy.dps
            }
        )
    except APIException as e:
        return Response(
            {'error': str(e)},
            status=e.status_code
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getImage(request):
    try:
        image_url = request.data.get('img_url')
        image_url = path.join(settings.MEDIA_ROOT, image_url)

        return FileResponse(
            open(image_url, 'rb'),
            content_type='image/jpg'
        )
    except APIException as e:
        return Response(
            {'error': str(e)},
            status=e.status_code
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
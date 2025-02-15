from kivy.uix.popup import Popup
from kivy.uix.label import Label
from requests.exceptions import *
import requests

from debug import logger


# 응답 코드를 저장한 예외 클래스
class ResponseException(RequestException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    def __str__(self):
        return '{} : {}'.format(self.code, self.message)
    def make_error_popup(self, title, content=None, size_hint=(1, 0.2), auto_dismiss=True, *args):
        if content == None:
            content = str(self)
        return Popup(
            title=title,
            content=Label(text=content),
            size_hint=size_hint,
            auto_dismiss=auto_dismiss,
            *args
        )

# 서버와의 인터페이스 베이스 클래스
class DBInterface:
    _url = 'http://127.0.0.1:8000/'
    # http 통신을 실행하는 함수. json()결과물이나 REsponseException()을 리턴만 하고, 예외를 발생시키지 않는다.
    def __execute(self, method, url, headers, data):
        try:
            response = method(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            return ResponseException(503, 'Failed to connect to the server.')
        except InvalidURL:
            return ResponseException(400, 'URL is invalid.')
        except Timeout as e:
            return ResponseException(408, 'The request timed out.')
        except HTTPError as e:
            return ResponseException(e.response.status_code, e.response.json().get('error'))
        except Exception as e:
            logger.error(str(e))
            return ResponseException(499, 'Internal client error')
    def _post(self, url, headers={}, data={}):
        return self.__execute(requests.post, url, headers, data)
    def _get(self, url, headers={}, data={}):
        return self.__execute(requests.get, url, headers, data)
    def _put(self, url, headers={}, data={}):
        return self.__execute(requests.put, url, headers, data)
    def _delete(self, url, headers={}, data={}):
        return self.__execute(requests.delete, url, headers, data)

class UsersDBInterface(DBInterface):
    def __init__(self):
        super(UsersDBInterface, self).__init__()
        self._url += 'users/'
        self.token = 'nothing'
        self.usernum = 0
    # 성공시 None, 실패시 Popup을 리턴
    def login(self, nickname, password):
        url = self._url + 'loginout/'
        data = {
            'nickname': nickname, 
            'password': password
        }

        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Login failed')

        self.token = response.get('token')
        self.usernum = response.get('usernum')
    # 성공시 None, 실패시 Popup을 리턴
    def logout(self):
        url = self._url + 'loginout/'
        headers = {
            'Autorization': 'Token ' + self.token
        }

        response = self._delete(url, headers=headers)

        if type(response) == ResponseException:
            return response.make_error_popup('Logout failed')

        self.token = ''
        self.usernum = 0
    # 성공시 None, 실패시 Popup을 리턴
    def signup(self, nickname, mailaddr, password):
        url = self._url + 'signupdown/'
        data = {
            'nickname': nickname, 
            'mailaddr': mailaddr, 
            'password': password
        }
        
        response = self._post(url, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Signup failed')
    # 성공시 None, 실패시 Popup을 리턴
    def signdown(self):
        url = self._url + 'signupdown/'
        headers = {
            'Authorization': 'Token ' + self.token
        }

        response = self._delete(url, headers=headers)

        if type(response) == ResponseException:
            return response.make_error_popup('Signdown failed')
    # 성공시 [...], 실패시 Popup을 리턴
    def get_charalist(self):
        url = self._url + 'charalist/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum
        }

        response = self._get(url, headers=headers, data=data)
        logger.info('Charanums are ' + str(response))

        if type(response) == ResponseException:
            if response.status_code == 404:
                return []
            else:
                return response.make_error_popup('Loading chara list failed')
        
        return response.get('charalist')
    # 성공시 None, 실패시 Popup을 리턴
    def post_chara(self, charanum):
        url = self._url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum
        }

        response = self._post(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Creating chara failed')
    # 성공시 {...}, 실패시 Popup을 리턴
    def get_chara(self, charanum):
        url = self._url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum
        }

        response = self._get(url, headers=headers, data=data)
        logger.info('Charainfo : ' + str(response))

        if type(response) == RequestException:
            if response.status_code == 404:
                return {}
            else:
                return response.make_error_popup('Loading chara failed')
        
        return response
    # 성공시 None, 실패시 Popup을 리턴
    def put_chara(self, charanum):
        lvl = self.get_charainfo(self.usernum, charanum).get('lvl') + 1
        atk = lvl * 10
        dps = lvl * 10

        url = self._url + 'chara/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            'charanum': charanum,
            'lvl': lvl,
            'atk': atk,
            'dps': dps
        }

        response = self._put(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Saving chara failed')
    # 성공시 None, 실패시 Popup을 리턴
    def post_item(self):
        url = self._url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
        }

        response = self._post(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Creating item error')
    # 성공시 아이템 갯수, 실패시 Popup을 리턴
    def get_item(self, item_name):
        url = self._url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum
        }

        response = self._get(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Loading item failed')
        
        return response.get(item_name)
    # 성공시 None, 실패시 Popup을 리턴
    def put_item(self, item_name, amount):
        url = self._url + 'item/'
        headers = {
            'Authorization': 'Token ' + self.token
        }
        data = {
            'usernum': self.usernum,
            item_name: amount,
        }

        response = self._put(url, headers=headers, data=data)

        if type(response) == ResponseException:
            return response.make_error_popup('Saving item error')
usersDBinterface = UsersDBInterface()

class EntitiesDBInterface(DBInterface):
    def __init__(self):
        super(EntitiesDBInterface, self).__init__()
        self._url += 'lessons/'
    def get_fullimg(self, charanum):
        return 'english_chan.jpg'
entitiesDBinterface = EntitiesDBInterface()

class LessonsDBInterface(DBInterface):
    def __init__(self):
        super(LessonsDBInterface, self).__init__()
        self._url += 'lessons/'
    def get_lessonmap_nums(self):
        url = self._url + 'lessonmaps/'

        result = self._get(url)
        if type(result) == Exception:
            return result
        
        return result.get('lessonmapnum')
    def get_lessonmap_info(self, lessonmapnum):
        url = self._url + 'lessonmap/'
        data = {
            'lessonmapnum': lessonmapnum
        }

        result = self._get(url, data=data)
        if type(result) == Exception:
            return result
        
        return result
lessonsDBinterface = LessonsDBInterface()
# -*- coding: utf-8 -*- 
from __future__ import print_function

from tornado.gen import coroutine
from tornado.escape import json_decode

from handlers.base_handler import BaseHandler
from model.user_model import UserModel


import sys
from operator import eq
sys.path.append('.')

from wrapper.route import route, authenticated
from utils.session_util import SessionUtil


@route('/api/async/v1/users')
class AuthHandler(BaseHandler):

    #获取用户列表
    @coroutine
    @authenticated
    def get(self):
        pass

    #新增用户
    @coroutine
    def post(self):
        user = UserModel()
        user_json = json_decode(self.request.body)

        user.user_name = user_json['user_name']
        user.name = user_json['user_name_cn']
        user.user_password = user_json['user_password']
        user.email = user_json['email']
        user.mobile = user_json['mobile']
        user.join_date = user_json['date']

        result = yield user.add_user()

        if result == 1:
            self.write(self.return_json(0, '已注册'))
        elif result == -1:
            self.write(self.return_json(-1, '用户名已存在'))

    #修改用户
    @coroutine
    @authenticated
    def patch(self):
        pass

    #删除用户
    @coroutine
    @authenticated
    def delete(self):
        pass


@route('/api/async/v1/user/login')
class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        user = UserModel()
        user_json = json_decode(self.request.body)
        user.user_name = user_json['user_name']
        user.user_password = user_json['user_password']

        user_exist = yield user.get_id_by_name()
        if user_exist == 0:
            self.write(self.return_json(-1, '用户名不存在'))
            return

        eq_password = yield user.get_password()
        if eq(eq_password, user.user_password):
            user_name = self.request.headers['User-Name']
            session_id = self.create_signed_value('user-key', user_name)
            session = SessionUtil(session_id, self.application.async_session_pool)
            yield session.set_session()
            self.set_secure_cookie('user-key', user_name, expires_days=1)
            self.write(self.return_json(0,'login'))
        else:
            self.write(self.return_json(1, '用户名或者密码错误'))


@route('/api/async/v1/user/logout')
class LogoutHandler(BaseHandler):
    @coroutine
    def delete(self):
        self.clear_cookie('cookie_id')
        sesssion = SessionUtil(self.get_current_user(), self.application.async_session_pool)
        yield sesssion.del_session()
        self.write(self.return_json(0,'clean'))


@route('/api/async/v1/user/status')
class UserHandler(BaseHandler):
    @coroutine
    def get(self):
        user_name = self.get_current_user()
        if user_name:
            self.write(self.return_json(0,'login'))
        else:
            self.write(self.return_json(1,'logout'))

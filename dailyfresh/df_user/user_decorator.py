#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# if not login redirect to login
def login(func):
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())  # zhuan dao yuan lai xiang qu de url
            return red
    return login_fun

"""
http://127.0.0.1/200/?type=10
requset.path : 表示当前路径-> /200/
request.get_full_path: 表示完整路径->/200/?type=10
"""
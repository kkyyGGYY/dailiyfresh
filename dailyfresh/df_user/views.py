# coding=utf-8
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
from . import user_decorator
from django.core.paginator import Paginator, Page
from df_goods.models import *
from df_orders.models import *

# import user_decorator


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两个密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转到登陆页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def register_email_exist(request):
    uemail = request.GET.get('uemail')
    count = UserInfo.objects.filter(uemail=uemail).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')

    context = {'title': '用户登陆', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)  # []是个列表
    print uname
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')  # 构造一个http的response,而且不直接return,因为接下来还要设置cookie
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    user_email = user.uemail
    user_address = user.uaddress
    user_phone = user.uphone
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    if len(goods_ids) != 0:
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(pk=int(goods_id)))
    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'user_address': user_address,
        'user_phone': user_phone,
        'page_name': 1,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, pindex):
    user = UserInfo.objects.get(id=request.session['user_id'])
    order = OrdersInfo.objects.filter(user_id=user)

    orderlist = []
    for o in order:
        oid = o.oid
        # print("-----------------oid", oid)
        ordersdetail = OrdersDetailInfo.objects.filter(order_id=oid)
        for i in ordersdetail:
            # print(i)
            orderlist.append(i)
    # print(orderlist)
    paginator = Paginator(order, 4)
    page = paginator.page(int(pindex))
    # print page
    # context = {
    #     'title': typeinfo.ttitle,
    #     'guest_cart': 1,
    #     'paginator': paginator,
    #     'typeinfo': typeinfo,
    #     'sort': sort,
    #     'news': news,
    #     'page': page,
    #     'count': count,
    # }
    context = {
        'title': '用户中心',
        'user_name': request.session['user_name'],
        'page_name': 1,
        'paginator': paginator,
        'page': page,
        'order': order,
        # 'ordersdetail': ordersdetail,
        'orderlist': orderlist,
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        post = request.POST
        user.ushou = post.get('ushou')
        user.uyoubian = post.get('uyoubian')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user, 'user_name': request.session['user_name'], 'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)


# coding=utf-8
from django.shortcuts import render, redirect
from models import *
from django.http import JsonResponse
from df_user import user_decorator
# Create your views here.


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'page_name': 1,
        'title': '购物车',
        'page_num': 1,
        'carts': carts,
    }
    print(uid)
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    # uid购买了gid商品，数量为count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车中是否已经有此商品，如果有就加数量，没有就新增
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    print('--------------------add--------------------')

    if len(carts) >= 1:
        cart = carts[0]
        cart.count += count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajsx请求则返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        count1 = cart.count
        cart.save()
        data = {'ok': 0}
        print('--------------------edit--------------------')
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)


@user_decorator.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
        print('-------------------delete-------------------')
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)

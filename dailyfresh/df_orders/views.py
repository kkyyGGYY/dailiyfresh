# coding=utf-8
from django.shortcuts import render, redirect
from models import *
from df_user import user_decorator
from df_user.models import *
from df_cart.models import *
from datetime import datetime
from django.db import transaction
# Create your views here.


@user_decorator.login
def order(request):
    # 查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    print('cart_ids', cart_ids)
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    print('carts', carts)
    # 构造传递到模板的数据
    context = {
        'title': '提交订单',
        'carts': carts,
        'user': user,
        'cart_ids': ','.join(cart_ids),
        'page_name': 1,
    }
    return render(request, 'df_orders/order.html', context)
'''
事物，一旦操作失败，操作回滚
1.创建订单对象
2.判断库存
3.创建详单对象
4.修改商品库存
5.删除购物车信息
'''


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接受购物车编号
    cart_ids = request.POST.getlist('cart_ids')
    print(cart_ids)
    try:
        # 创建订单对象
        order = OrdersInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        print(order.oid)
        order.odate = now
        order.ototal = request.POST.get('total')
        print request.POST.get('address')
        order.oaddress = request.POST.get('address')

        order.save()
        # 创建详单对象
        # cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids:
            print(id1)
            detail = OrdersDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断库存
            goods = cart.goods
            if goods.gkucun >= cart.count:
                # 减少库存
                goods.gkucun = cart.goods.gkucun - cart.count
                print(goods.gkucun)
                goods.save()

                # 完善详单信息
                # detail.user_id = uid
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车信息
                print('-----------------delete------------------')
                cart.delete()
            else:  # 购买数量大于库存
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('--------------%s--------------' % e)
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order_1/')


@user_decorator.login
def pay(request, oid):
    order = OrdersInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {'order': order}
    return render(request, 'df_order/pay.html', context)

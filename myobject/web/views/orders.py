# -*- coding:utf-8 -*-
# @Time    : 2021/12/27 11:02
# @Author  : Muzzily
# @desc    :
# -*- coding:utf-8 -*-
# @Time    : 2021/12/26 19:38
# @Author  : Muzzily
# @desc    : 购物车管理视图页面
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime
from myadmin.models import Orders, OrderDetail, Payment, User, Member


def index(request, pIndex=1):
    """浏览订单详情"""
    '''浏览订单信息'''
    omod = Orders.objects
    shop_id = request.session['shopinfo']['id']  # 店铺id号
    mywhere = []
    list = omod.filter(shop_id=shop_id)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 10)  # 以10条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    for vo in list2:
        if vo.user_id == 0:
            vo.nickname = "无"
        else:
            user = User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname = user.nickname

        if vo.member_id == 0:
            vo.membername = "大堂顾客"
        else:
            user = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = user.mobile
    # 封装信息加载模板输出
    context = {"orderslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere,
               'url': request.build_absolute_uri()}
    return render(request, "web/list.html", context)


def insert(request):
    """执行订单添加"""
    try:
        # 执行订单信息的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']  # 店铺id号
        od.member_id = 0  # 会员id
        od.user_id = request.session['webuser']['id']  # 操作员id
        od.money = request.session['total_money']
        od.status = 1  # 订单状态:1过行中/2无效/3已完成
        od.payment_status = 2  # 支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 执行支付信息
        op = Payment()
        op.order_id = od.id  # 订单id号
        op.member_id = 0
        op.type = 2
        op.bank = request.GET.get('bank', 3)
        op.money = request.session['total_money']
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()
        # 订单详情
        cartlist = request.session.get("cartlist", {})
        # 遍历购物车中的菜品并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = item['id']
            ov.product_name = item['name']
            ov.price = item['price']
            ov.quantity = item['num']
            ov.status = 1
            ov.save()
        del request.session['cartlist']
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        context = {"info": "订单添加失败，请稍后再试！"}
        return HttpResponse("N")


def detail(request):
    """加载订单详情"""
    oid = request.GET.get("oid", 0)

    # 加载订单详情
    dlist = OrderDetail.objects.filter(order_id=oid)
    # 遍历每个商品详情，从Goods中获取对应的图片
    # for og in dlist:
    #    og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

    # 放置模板变量，加载模板并输出
    context = {'detaillist': dlist}
    return render(request, "web/detail.html", context)


def status(request):
    """修改订单状态"""
    try:
        oid = request.GET.get("oid", '0')
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

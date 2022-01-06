# -*- coding:utf-8 -*-
# @Time    : 2021/12/27 16:16
# @Author  : Muzzily
# @desc    :
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from myadmin.models import Member, Shop, Category, Product, Orders, Payment, OrderDetail


def index(request):
    """个人中心首页"""
    return render(request, 'mobile/member.html')


def orders(request):
    """个人中心浏览订单"""
    ''' 个人中心浏览订单 '''
    mod = Orders.objects
    mid = request.session['mobileuser']['id']  # 获取当前会员id号
    olist = mod.filter(member_id=mid)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
    # 按id号做降序排序
    list2 = olist.order_by("-id")
    order_status = ["无", "排队中", "已撤销", "已完成"]
    # 遍历订单，关联其他表数据（订单详情，店铺信息）
    for vo in list2:
        plist = OrderDetail.objects.filter(order_id=vo.id)[:4]  # 获取前4条
        vo.plist = plist
        vo.statusinfo = order_status[vo.status]  # 转换订单状态

    return render(request, "mobile/member_orders.html", {"orderslist": list2})


def detail(request):
    """个人中心订单详情"""
    pid = request.GET.get("pid", 0)
    order = Orders.objects.get(id=pid)

    order_status = ["无", "排队中", "已撤销", "已完成"]
    # 获取关联其他表数据（订单详情，店铺信息）
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop = Shop.objects.only("name").get(id=order.shop_id)
    order.shopname = shop.name
    order.statusinfo = order_status[order.status]  # 转换订单状态

    return render(request, "mobile/member_detail.html", {"order": order})


def logout(request):
    """执行会员退出"""
    del request.session['mobileuser']
    return render(request, 'mobile/register.html')

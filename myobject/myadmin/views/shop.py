# -*- coding:utf-8 -*-
# @Time    : 2021/12/17 15:34
# @Author  : Muzzily
# @desc    :
import random
import time

from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Shop
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime


# Create your views here.
def index(request, pIndex=1):
    smod = Shop.objects
    slist = smod.filter(status__lt=9)  #
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        # 使用或的关系进行多条件查询
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)
    # 执行分页处理
    slist = slist.order_by("id")
    pIndex = int(pIndex)
    page = Paginator(slist, 5)  # 以每页5条数据分页
    maxpage = page.num_pages  # 得到多少页
    # 判断当前页是否越界
    if pIndex > maxpage:
        pIndex = maxpage
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    # 获取页码列表信息
    plist = page.page_range
    content = {"shoplist": list2, "plist": plist, 'pIndex': pIndex, 'maxpage': maxpage, 'mywhere': mywhere}
    return render(request, "myadmin/shop/index.html", content)


def add(request):
    """加载信息添加表单"""
    return render(request, 'myadmin/shop/add.html')


def insert(request):
    """执行信息添加"""
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 实例化model，封装信息，并执行添加
        ob = Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '添加成功!'}
    except Exception as e:
        print(e)
        content = {'info': "添加失败！"}
    return render(request, 'myadmin/info.html', content)


def delete(request, sid=0):
    """删除信息"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9  # 将转态改为9即可，便是删除操作
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '删除成功!'}
    except Exception as e:
        print(e)
        content = {'info': "删除失败！"}
    return render(request, 'myadmin/info.html', content)


def edit(request, sid):
    """编辑信息"""
    try:

        ob = Shop.objects.get(id=sid)

        content = {'shop': ob}
        return render(request, 'myadmin/shop/edit.html', content)
    except Exception as e:
        print(e)
        content = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', content)


def update(request, sid):
    """更新信息"""
    try:
        ob = Shop.objects.get(id=sid)
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if myfile:
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            ob.cover_pic = cover_pic

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if myfile:
            banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/" + banner_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            ob.banner_pic = banner_pic
        ob.status = request.POST['status']
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '修改成功!'}
    except Exception as e:
        print(e)
        content = {'info': "修改失败！"}
    return render(request, 'myadmin/info.html', content)

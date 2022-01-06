# -*- coding:utf-8 -*-
# @Time    : 2021/12/17 15:34
# @Author  : Muzzily
# @desc    :
import random
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime


# Create your views here.
def index(request, pIndex=1):
    umod = User.objects
    ulist = umod.filter(status__lt=9)  #
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        # 使用或的关系进行多条件查询
        ulist = ulist.filter(Q(username__contains=kw)) | ulist.filter(Q(nickname__contains=kw))
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 以每页5条数据分页
    maxpage = page.num_pages  # 得到多少页
    # 判断当前页是否越界
    if pIndex > maxpage:
        pIndex = maxpage
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    # 获取页码列表信息
    plist = page.page_range

    content = {"userlist": list2, "plist": plist, 'pIndex': pIndex, 'maxpage': maxpage, 'mywhere': mywhere}
    return render(request, "myadmin/user/index.html", content)


def add(request):
    """加载信息添加表单"""
    return render(request, 'myadmin/user/add.html')


def insert(request):
    """执行信息添加"""
    try:
        ob = User()
        ob.username = request.POST.get('username')
        ob.nickname = request.POST.get('nickname')
        # 将密码做MD5操作，将明文密码加密
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '添加成功!'}
    except Exception as e:
        print(e)
        content = {'info': "添加失败！"}
    return render(request, 'myadmin/info.html', content)


def delete(request, uid=0):
    """删除信息"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9  # 将转态改为9即可，便是删除操作
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '删除成功!'}
    except Exception as e:
        print(e)
        content = {'info': "删除失败！"}
    return render(request, 'myadmin/info.html', content)


def edit(request, uid):
    """编辑信息"""
    try:
        ob = User.objects.get(id=uid)
        content = {'user': ob}
        return render(request, 'myadmin/user/edit.html', content)
    except Exception as e:
        print(e)
        content = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', content)


def update(request, uid):
    """更新信息"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = request.POST['status']
        ob.nickname = request.POST['nickname']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '修改成功!'}
    except Exception as e:
        print(e)
        content = {'info': "修改失败！"}
    return render(request, 'myadmin/info.html', content)



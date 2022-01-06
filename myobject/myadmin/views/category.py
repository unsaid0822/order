# -*- coding:utf-8 -*-
# @Time    : 2021/12/20 22:03
# @Author  : Muzzily
# @desc    :
# -*- coding:utf-8 -*-
# @Time    : 2021/12/17 15:34
# @Author  : Muzzily
# @desc    :
import random

from django.http import JsonResponse
from django.shortcuts import render
from myadmin.models import Category, Shop
from django.core.paginator import Paginator
from datetime import datetime


# Create your views here.
def index(request, pIndex=1):
    umod = Category.objects
    ulist = umod.filter(status__lt=9)  #
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        # 使用或的关系进行多条件查询
        ulist = ulist.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以每页5条数据分页
    maxpage = page.num_pages  # 得到多少页
    # 判断当前页是否越界
    if pIndex > maxpage:
        pIndex = maxpage
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    # 获取页码列表信息
    plist = page.page_range

    # 遍历当前菜品分类信息，并封装对应的店铺信息
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
    content = {"categorylist": list2, "plist": plist, 'pIndex': pIndex, 'maxpage': maxpage, 'mywhere': mywhere}
    return render(request, "myadmin/category/index.html", content)


def add(request):
    """加载信息添加表单"""
    slist = Shop.objects.values("id", "name")
    content = {'shoplist': slist}
    return render(request, 'myadmin/category/add.html', content)


def insert(request):
    """执行信息添加"""
    try:
        ob = Category()
        ob.shop_id = request.POST.get('shop_id')
        ob.name = request.POST.get('name')
        ob.status = 1
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '添加成功!'}
    except Exception as e:
        print(e)
        content = {'info': "添加失败！"}
    return render(request, 'myadmin/info.html', content)


def delete(request, cid=0):
    """删除信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9  # 将转态改为9即可，便是删除操作
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '删除成功!'}
    except Exception as e:
        print(e)
        content = {'info': "删除失败！"}
    return render(request, 'myadmin/info.html', content)


def edit(request, cid):
    """编辑信息"""
    try:

        ob = Category.objects.get(id=cid)
        content = {'category': ob}
        slist = Shop.objects.values("id", "name")
        content['shoplist'] = slist
        return render(request, 'myadmin/category/edit.html', content)
    except Exception as e:
        print(e)
        content = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', content)


def update(request, cid):
    """更新信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.status = request.POST['status']
        ob.name = request.POST['name']
        ob.shop_id = request.POST['shop_id']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '修改成功!'}
    except Exception as e:
        print(e)
        content = {'info': "修改失败！"}
    return render(request, 'myadmin/info.html', content)


def loadCategory(request, sid):
    clist = Category.objects.filter(status__lt=9, shop_id=sid).values("id", "name")
    # 返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data': list(clist)})

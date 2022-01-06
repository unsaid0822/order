# -*- coding:utf-8 -*-
# @Time    : 2021/12/25 14:51
# @Author  : Muzzily
# @desc    :


# -*- coding:utf-8 -*-
# @Time    : 2021/12/17 15:34
# @Author  : Muzzily
# @desc    :
from django.shortcuts import render
from myadmin.models import Member
from django.core.paginator import Paginator
from datetime import datetime


# Create your views here.
def index(request, pIndex=1):
    umod = Member.objects
    ulist = umod.filter(status__lt=9)  #
    mywhere = []

    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    ulist = ulist.order_by('id')
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

    content = {"memberlist": list2, "plist": plist, 'pIndex': pIndex, 'maxpage': maxpage, 'mywhere': mywhere}
    return render(request, "myadmin/member/index.html", content)


def delete(request, uid=0):
    """删除信息"""
    try:
        ob = Member.objects.get(id=uid)
        ob.status = 9  # 将转态改为9即可，便是删除操作
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        content = {'info': '删除成功!'}
    except Exception as e:
        print(e)
        content = {'info': "删除失败！"}
    return render(request, 'myadmin/info.html', content)

# -*- coding:utf-8 -*-
# @Time    : 2021/12/19 21:04
# @Author  : Muzzily
# @desc    :
# 自定义中间类（执行是否登录判断）
from django.shortcuts import redirect
from django.urls import reverse
import re


class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print("url: %s" % path)
        # 定义后台不登录也可直接访问的url列表
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verify']
        # 判断当前请求url地址是否是以/myadmin开头,并且不在urllist中，才做是否登录判断
        if re.match(r'^/myadmin', path) and path not in urllist:
            # 判断管理后台是否登录
            # 判断是否登录(在于session中没有adminuser)
            if 'adminuser' not in request.session:
                # 重定向到登录页面
                return redirect(reverse('myadmin_login'))

        # 判断大堂点餐请求，是否登录
        if re.match(r'^/web', path) and path not in urllist:
            # 判断管理后台是否登录
            # 判断是否登录(在于session中没有adminuser)
            if 'webuser' not in request.session:
                # 重定向到登录页面
                return redirect(reverse('web_login'))

        # 判断移动端是否登录

        urllist = ['/mobile/register', '/mobile/doregister', ]
        # 判断当前请求url地址是否是以/mobile开头,并且不在urllist中，才做是否登录判断
        if re.match(r'^/mobile', path) and path not in urllist:
            # 判断管理后台是否登录
            # 判断是否登录(在于session中没有mobileuser)
            if 'mobileuser' not in request.session:
                # 重定向到登录页面
                return redirect(reverse('mobile_register'))

        response = self.get_response(request)
        return response

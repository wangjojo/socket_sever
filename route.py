#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-06-02 01:50:27
# @Author  : Wangjojo (wangjojo1995@gmail.com)
from utils import log

def error(request,code = '404'):
    error_list = {
        '404': b'HTTP/1.1 404 NOT_Found\r\n<h1>Page NOT Found</h1>'
    }

    response = error_list.get(code,b'')
    return response

def template(file_name):
    '''
    返回html资源
    '''    

    path = 'templates/' + file_name
    log(path)
    with open(path,'r',encoding = 'utf-8') as f:
        return f.read()

def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    file_name = request.query.get('file','123.jpg')
    path = 'static/' + file_name
    with open(path,'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        response = header + f.read()
        return response

def route_index(request):
    '''
    首页视图
    '''
    header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = template('index.html')
    response = header.decode('utf-8') + body
    return response.encode('utf-8')

def route_login(request):
    pass

def route_register(request):
    pass

def route_message(request):
    pass


route_dict = {
    '/static': route_static,
    '/': route_index,
    '/login': route_login,
    '/register':route_register,
    '/message':route_message,
}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-06-02 01:50:27
# @Author  : Wangjojo (wangjojo1995@gmail.com)
import socket
from urllib.parse import unquote

from utils import log
from route import route_dict
from route import route_static,error

class Request(object):
    """
    保存请求,需要保存的内容：method,path,query,body

    """
    def __init__(self):
        self.method = 'GET'
        self.path = ""
        self.query = {}
        self.body = ''
    #需要将body转化为dict,body形式：a=b&c=d 和query差不多
    #body这个时候为byte数据，需要解析
    def form(self):
        form = {}
        body = unquote(self.body)
        args = body.split('&')
        for arg in args:
            k,v = arg.split('=')
            form[k] = v
        return form

#接受请求
def request_accept(connection):
    r = []
    while True:
        result = connection.recv(1024)
        if result:
            r.append(result)
        r = r[0].decode('utf-8')

        return r
        
def parsed_request(req):
    #请求例子: 'GET / HTTP/1.1\r\nhost\r\n\r\nbody'
    request.method = req.split()[0]
    #解析path和query
    path = req.split()[1]
    if '?' not in path:
        request.path = path
    else:
        query = {}
        path,query_string = path.split('?')
        args = query_string.split('&')
        for arg in args:
            k,v = arg.split('=')
            query[k] = v
        request.path = path
        request.query =query

    body = req.split('\r\n\r\n',1)[1]
    request.body = body

#mvc-v
#构造response
def response_for_path(path):
    url_dict = {
        '/static': route_static,
    }
    #加载route
    url_dict.update(route_dict)
    #注意啊，这里是把一个函数赋予了response
    response = url_dict.get(path,error)
    return response(request)


#初始化全局request
request = Request()

def run(host='',port = 3000):
    log('服务器启动：{}:{}'.format(host,port))
    with socket.socket() as s:
    #s = socket.socket()
        s.bind((host,port))
        while True:
            s.listen(5)
            connection,address = s.accept()
            log('create connection:{}'.format(address))
            #处理请求并暂时保存，所以需要一个全局变量request
            #接受请求
            r = request_accept(connection)
            log('原始请求:{}'.format(r))
            #解析请求
            parsed_request(r) 

            response = response_for_path(request.path)
            connection.sendall(response)
            connection.close()

if __name__ == '__main__':
    config ={
        'host':'192.168.74.137',
        'port':3002,
    }
    run(**config)
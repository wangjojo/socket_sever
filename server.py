import socket
import urllib.parse

#保存用户请求
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    #把body转化为dict形式
    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k,v = arg.split('=')
            f[k] = v

        return f
#定义一个全局变量request
request = Request()

#解析路径
def parse_path(path):
    if '?' in path:
        path,query = path.split('?')
        #分离query后，构造dict
        query_dict = {}
        query_list = query.split('&')
        for each in query_list:
            k,v = each.split('=')
            query_dict[k] = v
        return path,query_dict
    else:
        return path,{}

def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')

#这里属于mvc的v
#构造response函数
def response_for_path(path):
    #解析请求路由
    path,query = parse_path(path)
    request.path = path
    request.query = query
    #调用相应函数
    r = {
        '/static': route_static,
    }
    #载入已有路由并查询
    r.update(route_dict)
    response = r.get(path,error)
    
    return response(request)


def run(host,port = 3000):
    with socket.socket() as s:
        s.bind((host,port))
        while True:
            #开始监听
            s.listen(5)
            #接受请求
            #请求和用户ip
            connection,address = s.accept()
            r = ''
            while True:
                result = connection.recv(1024)
                r += result
                if len(result) < 1024:
                    break
            r = r.decode('utf-8')
            if len(r.split()) < 2:
                continue

            path = r.split()[1]
            #请求路径可能还包含其他信息，要进一步处理
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n',1)[1]
            response = response_for_path(path)

            connection.sendall(response)
            connection.close()
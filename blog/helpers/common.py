# coding = utf-8
import urllib
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            if confirm_url(target):
                return redirect(target)
        return redirect(url_for(default, **kwargs))


def confirm_url(target):
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           test_url.netloc == request.host and \
           test_url.path != request.path


def find_dup(form, sql):
    '''
    处理SQLAlchemy多对多关系，找到其中的重复量
    :param form: form中的对象列表
    :param sql: sql中的对象列表
    :return :返回需要移除和添加的SQLAlchemy元素集合
    '''
    form_set = set(form)
    sql_set = set(sql)
    dup = form_set & sql_set
    remove_set = sql_set - dup
    add_set = form_set - dup
    return remove_set, add_set


def custom_cache_key():
    '''
    将请求url主机以后的查询参数的键/值排序后返回
    示例：'127.0.0.1:5000/post?q=1+3+2'将返回'/post?q=1+2+3',
    '127.0.0.1:5000/md/10'将返回'/md/10'
    返回结果不以'?'结尾，方便删除key时调用url_for()方法
    :return str:整理后的部分路径
    '''
    args = request.args
    if args:
        key = request.path + '?' + urllib.parse.urlencode([
            (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
        ])
    else:
        key = request.path
    return key

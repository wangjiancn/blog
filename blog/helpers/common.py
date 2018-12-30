# coding = utf-8
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app


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

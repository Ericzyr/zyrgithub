#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

cache = {}


def compute_key(function, args, kwargs):
    key = str(function) + str(args) + str(kwargs)
    # key = pickle.dumps((function.func_name, args, kwargs))
    return hashlib.sha1(key).hexdigest()


def memoize(function):
    """
    使用此修饰器修饰的方法,执行结果会被缓存起来.被修饰方法的相同参数的多次调用,被修饰方法只会执行一次
    修饰器详情参考: http://blog.csdn.net/tb6013245/article/details/45010503
    此方法参考: http://www.cnblogs.com/amghost/p/3572128.html
    """

    def wrapper(*args, **kwargs):

        key = compute_key(function, args, kwargs)

        if key in cache:
            return cache[key]

        result = function(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper
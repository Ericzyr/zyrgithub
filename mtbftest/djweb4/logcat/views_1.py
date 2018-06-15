#!/usr/bin/env python3
# -*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,Context,Template

def home(request):
    name = "hello haiyan"
    i = 200
    l = [11, 22, 33, 44, 55]
    d = {"name": "haiyan", "age": 20}

    class People(object):  # 继承元类
        def __init__(self , name , age):
            self.name = name
            self.age = age

        def __str__(self):
            return self.name + str(self.age)

        def dream(self):
            return "你有梦想吗？"

    # 实例化
    person_egon = People("egon", 10)
    person_dada = People("dada", 34)
    person_susan = People("susan", 34)
    person_list = [person_dada, person_egon, person_susan]

    # return render(request, 'home.html', locals())

    return render_to_response('home.html', {'name': person_egon.name})
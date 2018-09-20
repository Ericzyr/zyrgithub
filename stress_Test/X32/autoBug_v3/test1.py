#! /usr/bin/env python
#  -*- coding: utf-8 -*-
class Test:
    def prt(self):
        # print(runoob)
        # print(runoob.__class__.__name__)
        print "+++++"*10
    def __abs__(self):
        print ""


if __name__ == '__main__':
    a=Test()
    a.prt()

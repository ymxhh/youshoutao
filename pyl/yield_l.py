# coding=utf-8
'''
Created on 2018年7月24日

@author: 27419
'''
def simple_coroutine():
    print("waht's your name?")
    name = yield
    print("Hello", name, ", where are you from?")
    nation = yield
    print("OK, I see")
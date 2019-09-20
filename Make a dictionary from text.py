# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 10:29:15 2019

@author: 20786136
"""





def Dictionary(text):
    Text = text.split()
    d = dict()
    for word in Text:
        if word in d:
            d[word] = d[word] + 1
        else:
            d[word] = 1
    return d

Dictionary(News)
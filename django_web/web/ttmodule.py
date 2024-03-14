from django.shortcuts import render,redirect
from django import forms
from django.shortcuts import render
from utils.encrypt import md5

from django.core.paginator import  Paginator
from django.db.models import Q
from web import models
from django.http import JsonResponse




def tt_module(request):
    ''''数据库操作'''
    
    return render(request, "web/tt_module.html")

def chart_bar(request):
    legend =["sales"]
    series_list =[
        
        {
          "name": "sales",
          "type": "bar",
          "data": [5, 20, 36, 10, 10, 20],
        }
    ]
    x_axis = ["Shirts", "Cardigans", "Chiffons", "Pants", "Heels", "Socks"]

    result ={
        "status" : True,
        "data":{
            'legend' : legend,
            'series_list' : series_list,
            'x_axis' : x_axis,
        }
    }
    return JsonResponse(result)

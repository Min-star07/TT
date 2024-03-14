from django.shortcuts import render,redirect
from django import forms
from django.shortcuts import render
from utils.encrypt import md5

from django.core.paginator import  Paginator
from django.db.models import Q
from web import models

def useful(request):
    
    return render(request, "web/useful.html")

def gallery1(request):
    
    return render(request, "web/gallery1.html")

def video1(request):
    
    return render(request, "web/video1.html")

def int_link(request):
    
    return render(request, "web/int_link.html")


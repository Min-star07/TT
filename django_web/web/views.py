from django.shortcuts import render,redirect
from django import forms
from django.shortcuts import render
from utils.encrypt import md5

from django.core.paginator import  Paginator
from django.db.models import Q
from web import models

class LoginForm(forms.Form):
    username = forms.CharField(label ="Username", widget=forms.TextInput(
        attrs={"class":"form-control", "placeholder":"Enter your username or email"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter your password"}, render_value=True) )

# Create your views here.
def index(request):
    # return HttpResponse("welcom django")
    return render(request, "web/home.html")

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'web/login.html', {"form": form})
    form = LoginForm(data = request.POST)
    if not form.is_valid():
        return render(request, 'web/login.html', {"form": form})
    #验证码正确，去数据库验证用户和密码
    user = form.cleaned_data["username"]
    pwd = form.cleaned_data["password"]
    # print(user, pwd)                                                                                                                        
    user_object = models.User.objects.filter(username=user, password =pwd).first()
    if not user_object:
        # form.add_error("password", "invalid user or password")
        return render(request, 'web/login.html', {"form": form, "error": "invalid user or password"})
    request.session["info"] = { " name":user_object.username, "password" : user_object.password }
    request.session.set_expiry(60 * 60 * 24 * 7)                                                            
    return redirect('/home/')

def logout(request):
    # return HttpResponse("welcom django")
    request.session.clear()
    return redirect("/login/")

def tt_telescope_chart(request):
    list_pede_sta = []
    list_Q1_dis = []
    list_Q1_sta = []
    list_fit_result = []
    for i in range(0, 8):
        name_jpg = "pedestal_check" + str(i) + ".pdf"
        list_pede_sta.append(name_jpg)
    
    for i in range(0, 8):
        name_jpg = "ROB_" + str(i) + "_Q1vsChannel2.pdf"
        list_Q1_dis.append(name_jpg)

    for i in range(0, 8):
        name_jpg = "ROB_" + str(i) + "_Q1vsChannel1.pdf"
        list_Q1_sta.append(name_jpg)
    
    for i in range(0, 8):
        name_jpg = "ROB_" + str(i) + "_final_result.pdf"
        list_fit_result.append(name_jpg)

    return render(request, 'web/tt_telescope_chart.html', {"ped" : list_pede_sta, "Q1_dis" : list_Q1_dis, "Q1_sta" : list_Q1_sta, "fit": list_fit_result})
def tt_telescope_table(request):
    ''''数据库操作'''
    queryset = models.TT_tele_calibration.objects.all()
    # return HttpResponse("success")
    # print(queryset)
    return render(request, "web/tt_telescope_table.html", {"queryset": queryset})

# def tt_table(request):
#     ''''数据库操作'''
#     queryset = models.TT_calibration.objects.all()
#     # return HttpResponse("success")
#     # print(queryset)
#     return render(request, "web/tt_table.html", {"queryset": queryset})

def tt_table(request,pIndex=1):
   
    ulist = models.TT_calibration.objects.all()
    mywhere = []
    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询员工账号或昵称中只要含有关键字的都可以
        # ulist = ulist.filter(Q(SN__contains=kw) | Q(nickname__contains=kw))
        ulist = ulist.filter(Q(SN__contains=kw))
        mywhere.append("keyword=" + kw)
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 2000)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # print(maxpages)
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # list2 = User.objects.all() #获取所有信息
    # 封装信息加载模板输出
    context = {"pmtlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,'mywhere':mywhere}
    return render(request, 'web/tt_table.html', context)

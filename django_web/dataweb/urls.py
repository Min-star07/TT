"""dataweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views, ttmodule,other
urlpatterns = [
    # path('admin/', admin.site.urls),
    path ('login/', views.login),
    path ('logout/', views.logout),
    path ('home/', views.index),
    path ('tt_telescope_chart/', views.tt_telescope_chart),
    path ('tt_telescope_table/', views.tt_telescope_table),
    path ('tt_module/', ttmodule.tt_module),
    path ('chart/bar/', ttmodule.chart_bar),
    path ('tt_table/', views.tt_table),
    path ('useful_link/', other.useful),
    path ('gallery_link/', other.gallery1),
    path ('video_link/', other.video1),
    path ('interesting_link/', other.int_link),
]

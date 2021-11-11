from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [

    path('', views.index, name="Index"),
    path('insert/', views.insert,name="insert"),
    path('MakeOneCloud/', views.Make_one_cloud,name="Make_one_cloud"),
]

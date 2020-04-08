# coding: utf-8
from django.urls import path

from App.views import IndexView

urlpatterns = [
    path("index/", IndexView.as_view(), name="index")
 ]

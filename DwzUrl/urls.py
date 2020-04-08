# codoing: utf-8
from django.urls import path

from DwzUrl import views

urlpatterns = [
    path("<str:url_code>", views.dwz, name="dwz"),
]


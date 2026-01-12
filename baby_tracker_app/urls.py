from django.urls import path
from django.http import HttpResponse


def main_page(request):
    return HttpResponse("Welcome to Baby Tracker application")


urlpatterns = [
    path("main_page/", main_page),
]

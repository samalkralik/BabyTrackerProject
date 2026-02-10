from django.urls import path
from django.shortcuts import HttpResponse
from baby_tracker_app import views


def test_view(request, **kwargs):
    return HttpResponse("test page: " + request.path)


urlpatterns = [
    path("", views.index_view),
    path("login/", test_view),
    path("overview/", views.overview_view),
    path("overview/add/", views.baby_create_view),  # add_baby_view
    path("overview/<int:baby_id>/", views.baby_detail_view),
    path("overview/<int:baby_id>/feeding/", views.feeding_view),
    path("overview/<int:baby_id>/sleep/", views.sleep_view),
    path("overview/<int:baby_id>/growth/", views.growth_view),
]

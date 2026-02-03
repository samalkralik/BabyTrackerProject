from django.urls import path
from django.shortcuts import HttpResponse
from baby_tracker_app import views


def test_view(request, **kwargs):
    return HttpResponse("test page: " + request.path)


urlpatterns = [
    path("", views.index_view),
    path("login/", test_view),
    path("overview/", views.overview_view),
    path("overview/add/", test_view),  # add_baby_view
    path("overview/<int:baby_id>/", views.baby_detail_view),
    path("overview/<int:baby_id>/growth/", test_view),  # overview_id_growth_view
    path("overview/<int:baby_id>/feeding/", views.baby_feeding_view),
    path("overview/<int:baby_id>/sleep/", test_view),  # overview_id_sleep_view
]

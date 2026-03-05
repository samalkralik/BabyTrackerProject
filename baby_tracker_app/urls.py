from django.urls import path
from django.shortcuts import HttpResponse
from baby_tracker_app import views


def test_view(request, **kwargs):
    return HttpResponse("test page: " + request.path)


urlpatterns = [
    path("", views.index_view),
    path("overview/", views.overview_view),
    path("overview-ajax/", views.overview_ajax),
    path("overview-json/", views.overview_json),
    path("overview-htmx/", views.overview_htmx),
    path("overview-detail-htmx/", views.overview_detail_htmx),
    path("overview/add/", views.baby_create_view),
    path("overview/<int:baby_id>/", views.baby_detail_view),
    path("overview/<int:baby_id>/update/", views.baby_update_view),
    path("overview/<int:baby_id>/feeding/", views.feeding_view),
    path(
        "overview/<int:baby_id>/feeding/update/<int:feeding_id>/",
        views.feeding_update_view,
    ),
    path("overview/<int:baby_id>/sleep/", views.sleep_view),
    path(
        "overview/<int:baby_id>/sleep/update/<int:sleep_id>/", views.sleep_update_view
    ),
    path("overview/<int:baby_id>/growth/", views.growth_view),
    path(
        "overview/<int:baby_id>/growth/update/<int:growth_id>/",
        views.growth_update_view,
    ),
    path("accounts/profile/", views.profile_view),
]

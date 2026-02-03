from django.urls import path


def test_view(request, **kwargs):
    from django.shortcuts import HttpResponse

    return HttpResponse("test page: " + request.path)


urlpatterns = [
    path("", test_view),
    path("home/", test_view),
    path("login/", test_view),
    path("baby-overview/", test_view),
    path("baby-overview/add/", test_view),
    path("baby-overview/<int:baby_id>/", test_view),
    path("baby-overview/<int:baby_id>/growth/", test_view),
    path("baby-overview/<int:baby_id>/feeding/", test_view),
    path("baby-overview/<int:baby_id>/sleep/", test_view),
]

"""
- home page
  /home/

- log in/ sign in
 /login/

- dashboard
  /overview/
  /overview/add-baby/


- baby details
  /baby/{baby_id}/growth
  /baby/{baby_id}/feeding
"""

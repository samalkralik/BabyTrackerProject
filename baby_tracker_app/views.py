from django.shortcuts import render
from baby_tracker_app.models import Baby


def index_view(request):
    return render(request, "baby_tracker_app/index.html")


def overview_view(request):
    babies = Baby.objects.all()
    return render(
        request,
        "baby_tracker_app/overview.html",
        {"baby_name": "Sara Smith", "babies": babies},
    )


def baby_detail_view(request, baby_id):
    print(baby_id)
    return render(request, "baby_tracker_app/baby_detail.html")


def baby_feeding_view(request, baby_id):
    print(baby_id)
    return render(request, "baby_tracker_app/baby_feeding.html")

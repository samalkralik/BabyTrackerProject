from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from baby_tracker_app.models import Baby, Feeding, Sleep, Growth
from baby_tracker_app.forms import BabyTrackerForm, FeedingForm, SleepForm, GrowthForm


def index_view(request):
    return render(request, "baby_tracker_app/index.html")


@login_required
def baby_create_view(request):
    if request.method == "POST":

        form = BabyTrackerForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent = request.user
            instance.save()
            return redirect("/overview/")

        print(form.is_valid())
        print(form.cleaned_data)
    else:
        form = BabyTrackerForm()  # handles GET request

    """
    if request.method == "GET":
        form = BabyTrackerForm()
    else:
        form = BabyTrackerForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)  # form.save() vraci instanci
            instance.parent = request.user
            instance.save()
            print("instance.pk:", instance.pk)
            return redirect("/overview/")

        print(form.is_valid())
        print(form.cleaned_data)
    """
    # template_name = 'nazev_app/nazev_modulu_form.html
    return render(request, "baby_tracker_app/baby_tracker_form.html", {"form": form})


@login_required
def overview_view(request):
    babies = Baby.objects.filter(parent=request.user)
    # babies = Baby.objects.all()
    return render(
        request,
        "baby_tracker_app/overview.html",
        {"baby_name": "Sara Smith", "babies": babies},
    )


@login_required
def baby_detail_view(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)

    # the LATEST entry for each category to show a "Status"
    latest_feeding = Feeding.objects.filter(baby=baby).order_by("-time").first()
    latest_sleep = Sleep.objects.filter(baby=baby).order_by("-start_time").first()
    latest_growth = Growth.objects.filter(baby=baby).order_by("-date").first()

    context = {
        "baby": baby,
        "latest_feeding": latest_feeding,
        "latest_sleep": latest_sleep,
        "latest_growth": latest_growth,
    }
    return render(request, "baby_tracker_app/baby_detail.html", context)


@login_required
def feeding_view(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)

    if request.method == "POST":
        form = FeedingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.baby = baby
            instance.save()
            return redirect("feeding_view", baby_id=baby.id)
    else:
        form = FeedingForm()

    feedings = Feeding.objects.filter(baby=baby).order_by("-time")[:10]
    return render(
        request,
        "baby_tracker_app/feeding.html",
        {"baby": baby, "form": form, "feedings": feedings},
    )


@login_required
def sleep_view(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)

    if request.method == "POST":
        form = SleepForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.baby = baby
            instance.save()
            return redirect("sleep_view", baby_id=baby.id)
    else:
        form = SleepForm()

    sleeps = Sleep.objects.filter(baby=baby).order_by("-start_time")[:10]
    return render(
        request,
        "baby_tracker_app/sleep.html",
        {"baby": baby, "form": form, "sleeps": sleeps},
    )


@login_required
def growth_view(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)

    if request.method == "POST":
        form = GrowthForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.baby = baby
            instance.save()
            return redirect("growth_view", baby_id=baby.id)
    else:
        form = GrowthForm()

    growths = Growth.objects.filter(baby=baby).order_by("-date")

    return render(
        request,
        "baby_tracker_app/growth.html",
        {"baby": baby, "form": form, "growths": growths},
    )


"""
def baby_feeding_view(request, baby_id):
    print(baby_id)
    return render(request, "baby_tracker_app/baby_feeding.html")
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from baby_tracker_app.models import Baby, Feeding, Sleep, Growth
from baby_tracker_app.forms import BabyTrackerForm, FeedingForm, SleepForm, GrowthForm


def index_view(request):
    return render(request, "baby_tracker_app/index.html")


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

    if request.method == "POST":
        if "submit_feeding" in request.POST:

            feeding_form = FeedingForm(request.POST)

            if feeding_form.is_valid():
                instance = feeding_form.save(commit=False)
                instance.baby = baby
                instance.save()
                return redirect(
                    "baby_detail", baby_id=baby.id
                )  # instead of hardcoded path like /overview/5/

        elif "submit_sleep" in request.POST:

            sleep_form = SleepForm(request.POST)

            if sleep_form.is_valid():
                instance = sleep_form.save(commit=False)
                instance.baby = baby
                instance.save()
                return redirect("baby_detail", baby_id=baby.id)

        elif "submit_growth" in request.POST:

            growth_form = GrowthForm(request.POST)

            if growth_form.is_valid():
                instance = growth_form.save(commit=False)
                instance.baby = baby
                instance.save()
                return redirect("baby_detail", baby_id=baby.id)

    feeding_form = FeedingForm()
    sleep_form = SleepForm()
    growth_form = GrowthForm()

    # existing data to show in the tabs
    feedings = Feeding.objects.filter(baby=baby).order_by("-time")[:5]
    sleeps = Sleep.objects.filter(baby=baby).order_by("-start_time")[:5]
    growths = Growth.objects.filter(baby=baby).order_by("-date")[:5]

    context = {
        "baby": baby,
        "feeding_form": feeding_form,
        "sleep_form": sleep_form,
        "growth_form": growth_form,
        "feedings": feedings,
        "sleeps": sleeps,
        "growths": growths,
    }
    return render(request, "baby_tracker_app/baby_detail.html", context)


"""
def baby_feeding_view(request, baby_id):
    print(baby_id)
    return render(request, "baby_tracker_app/baby_feeding.html")
"""

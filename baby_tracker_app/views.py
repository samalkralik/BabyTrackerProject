from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from baby_tracker_app.models import Baby, Feeding, Sleep, Growth
from baby_tracker_app.forms import BabyTrackerForm, FeedingForm, SleepForm, GrowthForm


def index_view(request):
    return render(request, "baby_tracker_app/index.html")


def profile_view(request):
    return render(request, "baby_tracker_app/account.html")


@login_required
def baby_create_view(request):
    if request.method == "POST":

        form = BabyTrackerForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.parent = request.user
            instance.save()
            return redirect(f"/overview/")
    else:
        form = BabyTrackerForm()  # handles GET request

    return render(request, "baby_tracker_app/baby_tracker_form.html", {"form": form})


@login_required
def baby_update_view(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)

    if request.method == "POST":
        if "delete" in request.POST:
            baby.delete()
            return redirect("/overview/")

        form = BabyTrackerForm(request.POST, request.FILES, instance=baby)

        if form.is_valid():
            instance = form.save()
            return redirect(f"/overview/{baby_id}/")
    else:
        form = BabyTrackerForm(instance=baby)

    return render(
        request, "baby_tracker_app/baby_tracker_form.html", {"form": form, "baby": baby}
    )


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

            # if JS failed to set time, set it to now
            if not instance.time:
                from django.utils import timezone

                instance.time = timezone.now()

            instance.save()
            return redirect(request.path)
    else:
        form = FeedingForm()

    feeding_tracks = Feeding.objects.filter(baby=baby).order_by("-time")

    paginator = Paginator(feeding_tracks, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "baby_tracker_app/feeding.html",
        {"baby": baby, "form": form, "page": page},
    )


@login_required
def feeding_update_view(request, baby_id, feeding_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)
    feeding = get_object_or_404(Feeding, id=feeding_id, baby=baby)

    if request.method == "POST":
        if "delete" in request.POST:
            feeding.delete()
            # Redirect to the main feeding list for this baby
            return redirect(f"/overview/{baby_id}/feeding/")

        form = FeedingForm(request.POST, instance=feeding)
        if form.is_valid():
            form.save()
            return redirect(f"/overview/{baby_id}/feeding/")
    else:
        form = FeedingForm(instance=feeding)

    return render(
        request,
        "baby_tracker_app/feeding_update.html",
        {"baby": baby, "form": form, "feeding": feeding},
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
            return redirect(request.path)
    else:
        form = SleepForm()

    sleep_tracks = Sleep.objects.filter(baby=baby).order_by("-start_time")

    paginator = Paginator(sleep_tracks, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "baby_tracker_app/sleep.html",
        {
            "baby": baby,
            "form": form,
            "page": page,
        },
    )


@login_required
def sleep_update_view(request, baby_id, sleep_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)
    sleep = get_object_or_404(Sleep, id=sleep_id, baby=baby)

    if request.method == "POST":
        if "delete" in request.POST:
            sleep.delete()
            return redirect(f"/overview/{baby_id}/sleep/")

        form = SleepForm(request.POST, instance=sleep)
        if form.is_valid():
            form.save()
            return redirect(f"/overview/{baby_id}/sleep/")
    else:
        form = SleepForm(instance=sleep)

    return render(
        request,
        "baby_tracker_app/sleep_update.html",
        {"form": form, "baby": baby, "sleep": sleep},
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
            return redirect(request.path)
            # return redirect("/overview/{baby.id}/growth/", baby_id=baby.id)
    else:
        form = GrowthForm()

    growth_tracks = Growth.objects.filter(baby=baby).order_by("-date")

    paginator = Paginator(growth_tracks, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "baby_tracker_app/growth.html",
        {"baby": baby, "form": form, "page": page},
    )


@login_required
def growth_update_view(request, baby_id, growth_id):
    baby = get_object_or_404(Baby, id=baby_id, parent=request.user)
    growth = get_object_or_404(Growth, id=growth_id, baby=baby)

    if request.method == "POST":
        if "delete" in request.POST:
            growth.delete()
            return redirect(f"/overview/{baby_id}/growth/")

        form = GrowthForm(request.POST, instance=growth)
        if form.is_valid():
            form.save()
            return redirect(f"/overview/{baby_id}/growth/")
    else:
        form = GrowthForm(instance=growth)

    return render(
        request,
        "baby_tracker_app/growth_update.html",
        {"form": form, "baby": baby, "growth": growth},
    )


def overview_ajax(request):
    """html page for ajax example"""
    return render(request, "baby_tracker_app/overview_ajax.html")


def overview_htmx(request):
    """html page for htmx example"""
    return render(request, "baby_tracker_app/overview_htmx.html")


from django.http import JsonResponse


def overview_json(request):
    per_load = 2
    startFrom = int(request.GET.get("startFrom") or 0)
    until = startFrom + per_load

    babies = Baby.objects.values("name", "gender")
    babies = list(babies[startFrom:until])

    if len(babies) < per_load:
        next_url = None
    else:
        next_url = "/overview-json/?startFrom=" + str(until)

    return JsonResponse(
        {
            "babies": babies,
            "next": next_url,
        }
    )


def overview_detail_htmx(request):
    per_load = 2
    startFrom = int(request.GET.get("startFrom") or 0)
    until = startFrom + per_load

    babies = Baby.objects.all()
    babies = list(babies[startFrom:until])

    if len(babies) < per_load:
        next_url = None
    else:
        next_url = "/overview-json/?startFrom=" + str(until)

    return render(
        request,
        "baby_tracker_app/include/overview.html",
        {
            "babies": babies,
        },
    )

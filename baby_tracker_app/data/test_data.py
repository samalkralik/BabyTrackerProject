from baby_tracker_app.models import Growth, Baby
import datetime as dt


def create_growth_tracks():
    baby1 = Baby.objects.first()

    for n in range(1, 10):
        Growth.objects.create(
            baby=baby1,
            date=dt.date.today(),
            weight=n,
            note="Weight " + str(n),
        )

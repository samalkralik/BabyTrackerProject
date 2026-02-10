from django import forms
from baby_tracker_app.models import Baby, Growth, Feeding, Sleep


class BabyTrackerForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ["name", "note"]


class GrowthForm(forms.ModelForm):
    model = Growth
    fields = ["date", "weight", "height", "note"]


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ["time", "feed_type", "amount", "note"]


class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ["start_time", "end_time"]

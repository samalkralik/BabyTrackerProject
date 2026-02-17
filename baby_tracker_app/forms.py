from django import forms
from baby_tracker_app.models import Baby, Growth, Feeding, Sleep


class BabyTrackerForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ["name", "image", "note"]


class GrowthForm(forms.ModelForm):
    class Meta:
        model = Growth
        fields = ["date", "weight", "height", "note"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ["time", "feed_type", "amount", "note"]
        widgets = {"time": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

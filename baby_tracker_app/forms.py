from django import forms
from baby_tracker_app.models import Baby, Growth, Feeding, Sleep


class BabyTrackerForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ["name", "birth_date", "gender", "image", "note"]
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}


class GrowthForm(forms.ModelForm):
    class Meta:
        model = Growth
        fields = ["date", "weight", "height", "note"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = [
            "feed_type",
            "milk_type",
            "amount",
            "note",
            "time",
            "duration",
        ]

        widgets = {
            "time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "feed_type": forms.Select(attrs={"class": "form-select"}),
            "milk_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "ml / grams"}
            ),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # optional because they depend on feed_type
        self.fields["feed_type"].choices = [("", "Choose feeding type...")] + list(
            self.fields["feed_type"].choices
        )[1:]

        self.fields["milk_type"].required = False
        self.fields["amount"].required = False
        self.fields["duration"].required = False
        self.fields["time"].required = False
        self.fields["note"].required = False


class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

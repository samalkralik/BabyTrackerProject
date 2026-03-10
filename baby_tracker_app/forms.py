from django import forms
from baby_tracker_app.models import Baby, Growth, Feeding, Sleep
from datetime import timedelta, datetime


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
    end_time = forms.DateTimeField(
        label="End Time",
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )

    class Meta:
        model = Feeding
        fields = [
            "feed_type",
            "milk_type",
            "amount",
            "duration",
            "note",
            "time",
        ]
        labels = {
            "time": "Start Time",
        }
        widgets = {
            "time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "feed_type": forms.Select(
                attrs={"class": "form-select", "id": "id_feed_type"}
            ),
            "milk_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "ml / grams"}
            ),
            "duration": forms.HiddenInput(),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        start = self.cleaned_data.get("time")
        end = self.cleaned_data.get("end_time")

        if start and end and instance.feed_type in ["1", "2"]:
            if isinstance(start, str):
                start = datetime.fromisoformat(start)
            if isinstance(end, str):
                end = datetime.fromisoformat(end)

            duration = (end - start).total_seconds()
            instance.duration = int(max(0, duration))

        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        feed_type_field = self.fields["feed_type"]
        feed_type_field.choices = [("", "Choose feeding type...")] + list(
            feed_type_field.choices
        )[1:]

        optional_fields = [
            "milk_type",
            "amount",
            "duration",
            "note",
            "time",
        ]
        for field_name in optional_fields:
            self.fields[field_name].required = False

        if (
            self.instance
            and self.instance.pk
            and self.instance.time
            and self.instance.duration
        ):
            start_time = self.instance.time
            duration_in_seconds = self.instance.duration
            end_time = start_time + timedelta(seconds=duration_in_seconds)

            self.fields["end_time"].initial = end_time.strftime("%Y-%m-%dT%H:%M")


class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

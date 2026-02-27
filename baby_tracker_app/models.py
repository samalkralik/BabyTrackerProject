from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# heslo123

User = get_user_model()


class Baby(models.Model):
    GENDER_CHOICES = [
        ("M", "Boy"),
        ("F", "Girl"),
    ]

    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        blank=True, null=True, upload_to="baby_tracker_app_images/"
    )
    note = models.TextField(
        max_length=100, blank=True, help_text="e.g., hair and eye color, character"
    )

    def __str__(self):
        return self.name

    @property
    def age_display(self):
        if not self.birth_date:
            return "No birth date"

        today = timezone.now().date()
        birth = self.birth_date

        delta = today - birth
        total_days = delta.days

        if total_days < 0:
            return "Future birth"

        # 2. Show Days or Weeks for newborns
        if total_days < 7:
            return f"{total_days} days"

        if total_days < 30:
            weeks = total_days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''}"

        # 3. Calculate Years and Months
        years = today.year - birth.year
        months = today.month - birth.month

        # Adjust for months/years that haven't fully passed yet
        if today.day < birth.day:
            months -= 1

        if months < 0:
            years -= 1
            months += 12

        if years > 0:
            year_str = f"{years} year{'s' if years != 1 else ''}"
            month_str = f"{months} month{'s' if months != 1 else ''}"
            return f"{year_str} {month_str}"

        return f"{months} month{'s' if months > 1 else ''}"


class Growth(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(
        max_digits=4, null=True, decimal_places=2, help_text="Enter weight in kg"
    )
    height = models.DecimalField(
        max_digits=5, null=True, decimal_places=2, help_text="Enter height in cm"
    )
    note = models.TextField(
        max_length=200, blank=True, help_text="e.g., First Smile, Crawling, New word"
    )

    def __str__(self):
        return f"Growth record for {self.baby} on {self.date}"


class Sleep(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def sleep_duration(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            total_seconds = int(duration.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            return f"{hours}h {minutes}m"
        return "0h 0m"

    def __str__(self):
        return f"{self.baby} slept for {self.sleep_duration}"


class FeedingType(models.IntegerChoices):
    LEFT_BREAST = 1, "Left Breast"
    RIGHT_BREAST = 2, "Right Breast"
    BOTTLE = 3, "Bottle"
    SOLID = 4, "Solid"


class MilkType(models.TextChoices):
    FORMULA = "formula", "Formula"
    BREAST_MILK = "breast_milk", "Breast Milk"


class Feeding(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    time = models.DateTimeField()
    feed_type = models.PositiveSmallIntegerField(choices=FeedingType.choices)
    milk_type = models.CharField(
        max_length=20, choices=MilkType.choices, blank=True, null=True
    )
    duration = models.PositiveIntegerField(blank=True, null=True)
    amount = models.FloatField(help_text="Amount in ml or grams", blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    @property
    def formatted_time(self):
        return self.time.strftime("%H:%M")

    def __str__(self):
        return f"{self.baby}'s feeding at {self.formatted_time}"

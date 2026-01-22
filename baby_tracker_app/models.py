from django.db import models
from django.contrib.auth import get_user_model

# heslo123

User = get_user_model()


class Baby(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    note = models.TextField(
        max_length=200, blank=True, help_text="e.g., hair and eye color, character"
    )

    def __str__(self):
        return self.name


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
    BREAST = 1, "Breast"
    BOTTLE = 2, "Bottle"
    SOLID = 3, "Solid"


class Feeding(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    time = models.DateTimeField()

    feed_type = models.PositiveSmallIntegerField(
        choices=FeedingType.choices,
        default=FeedingType.BREAST,
    )

    amount = models.FloatField(help_text="Amount in ml or grams")
    note = models.TextField(blank=True)

    @property
    def formatted_time(self):
        return self.time.strftime("%H:%M")

    def __str__(self):
        return f"{self.baby}'s feeding at {self.formatted_time}"

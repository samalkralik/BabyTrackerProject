from django.db import models
from django.contrib.auth import get_user_model

# heslo123

User = get_user_model()


class Baby(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="My baby")
    birth_date = models.DateField()
    weight = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, help_text="Enter birth weight in kg"
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, help_text="Enter birth height in cm"
    )
    notes = models.TextField(
        max_length=200, blank=True, help_text="e.g., hair and eye color, character"
    )

    def __str__(self):
        return self.name


class GrowthMilestones(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(
        max_digits=4, null=True, decimal_places=2, help_text="Enter weight in kg"
    )
    height = models.DecimalField(
        max_digits=5, null=True, decimal_places=2, help_text="Enter height in cm"
    )
    milestone_note = models.TextField(
        max_length=200, blank=True, help_text="e.g., First Smile, Crawling, New word"
    )

    def __str__(self):
        return f"Growth record for {self.baby} on {self.date}"


class Sleep(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.baby} slept for {self.end_time - self.start_time}"


class Feeding(models.Model):
    FEED_TYPES = [("breast", "Breast"), ("bottle", "Bottle"), ("solid", "Solid")]
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    feed_type = models.CharField(max_length=10, choices=FEED_TYPES)
    amount = models.FloatField(help_text="Amount in ml or grams")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.baby}'s last feeding was at {self.time}"

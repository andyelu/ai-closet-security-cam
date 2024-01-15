from django.db import models

class Event(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    image_data = models.CharField(max_length=200)

    def __str__(self):
        return self.time + " " + self.image_data


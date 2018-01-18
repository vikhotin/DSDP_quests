from django.db import models
from django.contrib.postgres.fields import ArrayField


class Token(models.Model):
    client_id = models.CharField(max_length=40)
    client_secret = models.CharField(max_length=128)
    token = models.CharField(max_length=30, null=True)
    expires = models.DateTimeField(null=True)


class Quest(models.Model):
    user_id = models.IntegerField()
    places_ids = ArrayField(models.IntegerField())
    puzzles_ids = ArrayField(models.IntegerField())
    cur_task = models.IntegerField()
    completed = models.BooleanField()

    def to_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "places_ids": str(self.places_ids),
            "puzzles_ids": str(self.puzzles_ids),
            "cur_task": str(self.cur_task),
            "completed": str(self.completed),
        }

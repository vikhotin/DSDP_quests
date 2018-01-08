from django.db import models
from django.contrib.postgres.fields import ArrayField


class Quest(models.Model):
    user_id = models.IntegerField()
    places_ids = ArrayField(models.IntegerField())
    puzzles_ids = ArrayField(models.IntegerField())
    cur_task = models.IntegerField()
    completed = models.BooleanField()

    def to_json(self):
        return {
            "user_id": str(self.user_id),
            "places_ids": str(self.places_ids),
            "puzzles_ids": str(self.puzzles_ids),
            "cur_task": str(self.cur_task),
            "completed": str(self.completed),
        }

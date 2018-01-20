from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    username = models.CharField(max_length=40)
    token = models.CharField(max_length=30, null=True)
    expires = models.DateTimeField(null=True)


# Site user model
class MyUser(models.Model):
    # login = models.CharField(max_length=25, unique=True)
    # password = models.CharField(max_length=30)
    # name = models.CharField(max_length=35)
    user = models.OneToOneField(User, models.CASCADE)
    quests_number = models.IntegerField(default=0)
    quests_completed = models.IntegerField(default=0)

    def to_json(self):
        s = {
            "id": str(self.id),
            "login": str(self.user.username),
            "name": str(self.user.first_name),
            "quests_number": str(self.quests_number),
            "quests_completed": str(self.quests_completed),
        }
        return s

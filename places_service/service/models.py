from django.db import models


# Place in city model
class Place(models.Model):
    name = models.CharField(max_length=100)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)

    def to_json(self):
        return {
            "name": str(self.name),
            "longitude": str(self.long),
            "latitude": str(self.lat),
        }


# Fact about place model
class Fact(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    text = models.TextField()
    is_moderated = models.BooleanField()


# Puzzle for the place model
class Puzzle(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.CharField(max_length=100)
    is_moderated = models.BooleanField()

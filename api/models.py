from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = "places"

    def __str__(self) -> str:
        """
        The method returns a string representation of the `Place` model instance.
        """
        return (
            f"Place(name={self.name}, "
            f"description={self.description}, "
            f"geom={self.geom})"
        )

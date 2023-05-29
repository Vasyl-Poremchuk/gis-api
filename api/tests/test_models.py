from django.test import TestCase

from api.models import Place


class ModelsTests(TestCase):
    def test_place_str(self) -> None:
        place = Place.objects.create(
            name="Central Park",
            description="Central Park is an iconic urban park located in Manhattan, "
            "New York City. It is known for its vast green spaces, "
            "picturesque landscapes, and numerous recreational activities. "
            "The park offers a peaceful retreat from the bustling city life "
            "and attracts millions of visitors each year.",
            geom="SRID=4326;POINT (40.7829 -73.9654)",
        )

        self.assertEquals(
            str(place),
            f"Place(name={place.name}, description={place.description}, geom={place.geom})",
        )

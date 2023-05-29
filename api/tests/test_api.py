from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from api.models import Place
from api.serializers import PlaceSerializer

PLACE_LIST_URL = reverse("api:place-list")


class ApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.first_place = Place.objects.create(
            name="Eiffel Tower",
            description="The Eiffel Tower is a wrought-iron lattice tower situated in Paris, "
            "France. It is one of the world's most recognizable landmarks and "
            "a symbol of the city. Standing at a height of 330 meters, the tower offers "
            "breathtaking views of Paris and has become a popular tourist attraction.",
            geom="SRID=4326;POINT (48.8584 2.2945)",
        )
        self.second_place = Place.objects.create(
            name="Great Wall of China",
            description="The Great Wall of China is an ancient fortification that stretches "
            "across Northern China. Built over several centuries, it is one of "
            "the most remarkable engineering feats in history. The wall served "
            "as a defensive structure and spans thousands of miles, showcasing "
            "breathtaking views of the surrounding landscapes.",
            geom="SRID=4326;POINT (40.4319 116.5704)",
        )

    def test_list_places(self) -> None:
        response = self.client.get(PLACE_LIST_URL)
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_create_place(self) -> None:
        payload = {
            "name": "Taj Mahal",
            "description": "The Taj Mahal is an ivory-white marble mausoleum located in Agra, India. "
            "It was built by the Mughal emperor Shah Jahan in memory of his beloved wife. "
            "Considered a masterpiece of Islamic architecture, the Taj Mahal is renowned "
            "for its intricate detailing, symmetry, and stunning beauty.",
            "geom": "SRID=4326;POINT (27.175 78.0422)",
        }
        response = self.client.post(PLACE_LIST_URL, payload)
        place = Place.objects.get(name="Taj Mahal")
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_place(self) -> None:
        place_detail_url = reverse(
            "api:place-detail",
            kwargs={"pk": self.first_place.pk},
        )
        response = self.client.get(place_detail_url)
        place = Place.objects.get(pk=self.first_place.pk)
        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_place(self) -> None:
        place_detail_url = reverse(
            "api:place-detail",
            kwargs={"pk": self.second_place.pk},
        )
        payload = {
            "name": "Sydney Opera House",
            "description": "The Sydney Opera House is a multi-venue performing arts center located in "
            "Sydney, Australia. Its unique design, featuring sail-like structures, "
            "has made it an architectural masterpiece. The Opera House hosts a wide range "
            "of cultural performances and events and is recognized as one of the most famous "
            "and distinctive buildings in the world.",
            "geom": "SRID=4326;POINT (-33.8568 151.2153)",
        }
        response = self.client.put(place_detail_url, payload)
        place = Place.objects.get(pk=self.second_place.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(place.name, payload["name"])
        self.assertEqual(place.description, payload["description"])
        self.assertEqual(place.geom, payload["geom"])

    def test_partial_update_place(self) -> None:
        place_detail_url = reverse(
            "api:place-detail",
            kwargs={"pk": self.first_place.pk},
        )
        payload = {"geom": "SRID=4326;POINT (151.2153 -33.8568)"}
        response = self.client.patch(place_detail_url, payload)
        place = Place.objects.get(pk=self.first_place.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(place.geom, payload["geom"])

    def test_delete_place(self) -> None:
        place_detail_url = reverse(
            "api:place-detail",
            kwargs={"pk": self.second_place.pk},
        )
        response = self.client.delete(place_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Place.objects.filter(pk=self.second_place.pk).exists()
        )

    def test_retrieve_nearest_place(self) -> None:
        response = self.client.get(
            "/api/places/nearest-place/",
            {"latitude": 2.2945, "longitude": 48.8584},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), self.first_place.name)

        self.first_place.delete()
        self.second_place.delete()

        response = self.client.get(
            "/api/places/nearest-place/",
            {"latitude": 116.5704, "longitude": 40.4319},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("message"), "Nearest place not found."
        )

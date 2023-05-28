from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Place
from api.serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


@api_view(["GET"])
def get_nearest_place(request: Request) -> Response:
    latitude = float(request.GET.get("latitude"))
    longitude = float(request.GET.get("longitude"))
    place = Point(longitude, latitude, srid=4326)

    nearest_place = (
        Place.objects.annotate(distance=Distance("geom", place))
        .order_by("distance")
        .first()
    )

    if not nearest_place:
        return Response({"message": "Nearest place not found."})

    return Response({"message": nearest_place.name})

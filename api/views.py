from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Place
from api.serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class GetNearestPlace(APIView):
    serializer_class = PlaceSerializer

    def get(self, request: Request) -> Response:
        latitude = float(request.GET.get("latitude"))
        longitude = float(request.GET.get("longitude"))
        place = Point(longitude, latitude, srid=4326)

        nearest_place = (
            Place.objects.annotate(distance=Distance("geom", place))
            .order_by("distance")
            .first()
        )

        if not nearest_place:
            return Response(
                {"message": "Nearest place not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": nearest_place.name}, status=status.HTTP_200_OK
        )

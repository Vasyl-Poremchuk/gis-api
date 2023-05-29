from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.utils import OpenApiParameter, extend_schema
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude",
                description="Point latitude",
                required=False,
                type=float,
                default=0,
            ),
            OpenApiParameter(
                name="longitude",
                description="Point longitude",
                required=False,
                type=float,
                default=0,
            ),
        ]
    )
    def get(self, request: Request) -> Response:
        """
        The method returns the `name` of the nearest `Place`
        according to the given coordinates.
        """
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

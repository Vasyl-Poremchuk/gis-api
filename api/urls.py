from django.urls import path

from api.views import GetNearestPlace, PlaceDetail, PlaceList


urlpatterns = [
    path("places/", PlaceList.as_view(), name="place-list"),
    path("places/<int:pk>/", PlaceDetail.as_view(), name="place-detail"),
    path(
        "places/nearest-place/",
        GetNearestPlace.as_view(),
        name="nearest-place",
    ),
]

app_name = "api"

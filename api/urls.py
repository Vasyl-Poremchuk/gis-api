from django.urls import path

from api.views import PlaceDetail, PlaceList, get_nearest_place


urlpatterns = [
    path("places/", PlaceList.as_view(), name="place-list"),
    path("places/<int:pk>/", PlaceDetail.as_view(), name="place-detail"),
    path("places/nearest-place/", get_nearest_place, name="nearest-place"),
]

app_name = "api"

from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.models import Place


class PlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Place
        geo_field = "geom"
        fields = ("id", "name", "description")

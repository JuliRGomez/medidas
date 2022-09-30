from rest_framework.serializers import ModelSerializer
from measures.models import Measures


class MeasuresSerializer(ModelSerializer):

    class Meta:
        model = Measures
        fields = '__all__'
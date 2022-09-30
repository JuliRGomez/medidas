from rest_framework.viewsets import ModelViewSet
from measures.models import Measures
from measures.serializers import MeasuresSerializer



class MeasuresViewSet(ModelViewSet):
    queryset = Measures.objects.all()
    serializer_class = MeasuresSerializer

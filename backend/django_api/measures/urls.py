from rest_framework.routers import DefaultRouter
from measures.views import MeasuresViewSet
router = DefaultRouter()
router.register(r'measures', MeasuresViewSet)

urlpatterns = router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TodoViewSet

router = DefaultRouter()
router.register('todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls))
]

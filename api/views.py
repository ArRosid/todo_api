from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import Todo
from api.serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (IsAuthenticated,)

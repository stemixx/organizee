from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Board
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Board.objects.filter(owner=user)
        else:
            raise PermissionDenied("You do not have permission to show this board.")
            # return Board.objects.none()

    def perform_create(self, serializer):
        # Автоматически назначаем текущего пользователя владельцем доски
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Проверка на то, что только владелец может обновить доску
        board = self.get_object()
        if board.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this board.")
        serializer.save()

    def perform_destroy(self, instance):
        # Проверка на то, что только владелец может удалить доску
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this board.")
        instance.delete()

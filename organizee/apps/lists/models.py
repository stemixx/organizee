from django.db import models
from apps.boards.models import Board


class List(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, related_name='lists', on_delete=models.CASCADE)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

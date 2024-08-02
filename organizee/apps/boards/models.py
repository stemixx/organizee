from django.db import models
from apps.users.models import CustomUser


class Board(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, default='My Board')
    description = models.TextField(blank=True)
    owner = models.ForeignKey(CustomUser, related_name='members', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BoardMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    board = models.ForeignKey(Board, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='board_memberships', on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('board', 'user')

    def __str__(self):
        return f'{self.user.email} - {self.role}'


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # HEX код цвета
    board_id = models.ForeignKey(Board, related_name='labels', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

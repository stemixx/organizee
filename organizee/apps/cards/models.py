from django.db import models
from apps.users.models import CustomUser
from apps.lists.models import List
from apps.boards.models import Label


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list_id = models.ForeignKey(List, related_name='cards', on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CardMember(models.Model):
    card = models.ForeignKey(Card, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='card_memberships', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.card.title}"


class CardLabel(models.Model):
    card = models.ForeignKey(Card, related_name='labels', on_delete=models.CASCADE)
    label = models.ForeignKey(Label, related_name='card_labels', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.card.title} - {self.label.name}"


class Comment(models.Model):
    content = models.TextField()
    card = models.ForeignKey(Card, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}..."

from django.contrib import admin
from django import forms
from .models import Board, BoardMember, Label


# ModelForms для моделей
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'owner']


class BoardMemberForm(forms.ModelForm):
    class Meta:
        model = BoardMember
        fields = ['board', 'user', 'role']


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color', 'board_id']


# Админ-классы для моделей
class BoardAdmin(admin.ModelAdmin):
    form = BoardForm
    list_display = ['name', 'owner', 'created_at', 'updated_at']
    search_fields = ['name', 'owner__email']


class BoardMemberAdmin(admin.ModelAdmin):
    form = BoardMemberForm
    list_display = ['board', 'user', 'role']
    search_fields = ['board__name', 'user__email']
    list_filter = ['role']


class LabelAdmin(admin.ModelAdmin):
    form = LabelForm
    list_display = ['name', 'color', 'board_id']
    search_fields = ['name', 'board_id__name']


# Регистрация моделей в админ-панели
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardMember, BoardMemberAdmin)
admin.site.register(Label, LabelAdmin)

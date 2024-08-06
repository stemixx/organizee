from django.urls import path
from rest_framework import routers
from .views import BoardViewSet, boards_list_view


router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
urlpatterns = [
    path('boards_list/', boards_list_view, name='boards_list'),
]
urlpatterns += router.urls

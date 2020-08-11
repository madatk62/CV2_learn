from django.urls import path
from .views import ImageViews
urlpatterns = [
    path('images', ImageViews.as_view(), name='image')
]
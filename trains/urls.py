from django.urls import path
from .views import add_train

urlpatterns = [
    path('add/', add_train, name='addTrain'),
]

from django.urls import path
from .views import add_train, update_train

urlpatterns = [
    path('add/', add_train, name='addTrain'),
    path('update/<int:trainId>/', update_train, name='updateTrain'),
]

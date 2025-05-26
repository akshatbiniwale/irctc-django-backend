from django.urls import path
from .views import add_train, update_train, delete_train, get_train

urlpatterns = [
    path('add/', add_train, name='addTrain'),
    path('update/<int:trainId>/', update_train, name='updateTrain'),
    path('delete/<int:trainId>/', delete_train, name='deleteTrain'),
    path('all/', get_train, name='getTrain'),
]

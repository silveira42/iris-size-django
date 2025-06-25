from django.urls import path
from .views import home, update, export

urlpatterns = [
    path('', home, name="home"),
    path('update', update, name="update"),
    path('export', export, name="export"),
]
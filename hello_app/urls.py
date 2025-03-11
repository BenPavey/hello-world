from django.urls import path
from hello_app import views

from hello_app.views import test_db


urlpatterns = [
    path("", views.home, name="home"),

    
    path("test-db/", test_db),





]
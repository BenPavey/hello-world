from django.urls import path
from hello_app import views


from .views import debug_static_files

urlpatterns = [
    path("", views.home, name="home"),
    path("debug-static/", debug_static_files, name="debug_static_files"),

]
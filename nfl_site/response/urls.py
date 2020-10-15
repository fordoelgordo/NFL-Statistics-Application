from django.urls import path
from django.conf.urls import url
from response import views

app_name = 'response'
urlpatterns = [
    path('', views.index, name = 'index'),
    # Create NFL/ path with image upon button click
    path('NFL/', views.click_button, name = 'click_button')
]
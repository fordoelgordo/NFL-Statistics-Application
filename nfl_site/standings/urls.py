from django.urls import path
from django.conf.urls import url
from standings import views

app_name = 'standings'
urlpatterns = [
    path('standingspage/', views.standings_page, name='standings_page'),
]
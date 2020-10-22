from django.urls import path
from django.conf.urls import url
from receiving import views

app_name = 'receiving'
urlpatterns = [
    path('', views.recieving_page, name='recieving_page'),
]

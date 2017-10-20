
from django.conf.urls import url,include
from app01 import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'p1/$', views.page1),
    url(r'p1_1/$', views.page1_1),
    url(r'^book/$',views.book),
]

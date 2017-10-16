
from django.conf.urls import url,include
from stu_crm import views
urlpatterns = [
    url(r'^$',views.dashboard),
    url(r'^customers/$',views.customers),
    url(r'^customers/(\d+)/$',views.customer_detail),
]


from django.conf.urls import url,include
from stu_crm import views
urlpatterns = [
    url(r'^$',views.dashboard),
    url(r'^customers/$',views.customers,name='customer_list'),
    url(r'^customers/(\d+)/$',views.customer_detail,name="customer_detail"),#可以起别名，前端动态调用，实现耦合<td><a href="{% url 'customer_detail' customer.id %}">{{ customer.id }}</a></td>
]

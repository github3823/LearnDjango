from django.shortcuts import render
from stu_crm import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from stu_crm import forms
# Create your views here.
def dashboard(request):
    return render(request,'stu_crm/crm/dashboard.html')

def customers(request):#前端分页
    customer_list = models.Customer.objects.all()
    paginator = Paginator(customer_list,5)
    page = request.GET.get('page')
    try:
        customer_objs = paginator.page(page)#返回指定页
    except PageNotAnInteger:#如果请求错误返回第一页
        customer_objs = paginator.page(1)#报错返回第一页
    except EmptyPage:#如果请求过界返回最后一页
        customer_objs = paginator.page(paginator.num_pages)


    return render(request,'stu_crm/crm/customers.html',{'customer_list' : customer_objs})
def customer_detail(request,customer_id):
    customer_obj= models.Customer.objects.get(id=customer_id)
    form = forms.CustomerModelForm(instance=customer_obj)#传入已有数据
    return  render(request,'stu_crm/crm/customer_detail.html',{'customer_form':form})
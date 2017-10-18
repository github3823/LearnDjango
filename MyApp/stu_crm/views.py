from django.shortcuts import render,redirect
from stu_crm import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from stu_crm import forms
from stu_crm.permissions import check_permission
# Create your views here.
def dashboard(request):
    return render(request,'stu_crm/crm/dashboard.html')

@check_permission
def customers(request):#前端分页,显示列表
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

@check_permission
def customer_detail(request,customer_id):
    customer_obj= models.Customer.objects.get(id=customer_id)
    if request.method == "POST":
        form = forms.CustomerModelForm(request.POST,instance=customer_obj)#告诉新录入的修改谁
        #print(request.POST)
        if form.is_valid():#判断值是否有效
            form.save()#有效就保存
            print('url:',request.path)
            base_url = "/".join(request.path.split("/")[:-2])#动态返回列表页
            print("url:",base_url)

            return redirect(base_url)#保存成功后返回列表页
    else:
        form = forms.CustomerModelForm(instance=customer_obj)#传入已有数据

    return  render(request,'stu_crm/crm/customer_detail.html',{'customer_form':form})
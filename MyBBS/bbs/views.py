from django.shortcuts import render,HttpResponseRedirect
from bbs import models
from django.contrib.auth import login,logout,authenticate #用户验证相关
from django.contrib.auth.decorators import login_required
# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')

def index(request):
    category_obj = models.Category.objects.get(position_index=1)
    article_list = models.Article.objects.filter(status='published')
    return render(request,'bbs/html/index.html',{'category_list':category_list,
                                                 'article_list':article_list,
                                                 'category_obj': category_obj,
                                                 })

def category(request,id):
    category_obj = models.Category.objects.get(id=id)
    if category_obj.position_index == 1:#首页
        article_list = models.Article.objects.filter(status='published')
    else:
        article_list = models.Article.objects.filter(category_id= category_obj.id,status='published')

    return render(request, 'bbs/html/index.html', {'category_list': category_list,
                                                   'category_obj': category_obj,
                                                   'article_list':article_list,
                                                   })


def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request,user)#登录用户
            return HttpResponseRedirect('/bbs')
        else:
            login_err = 'Wrong username or password!'
            return render(request,'bbs/html/login.html',{'login_err':login_err})

    return  render(request,'bbs/html/login.html')

def acc_logout(request):
    logout(request)
    return  HttpResponseRedirect('/bbs')
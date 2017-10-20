from django.shortcuts import render,HttpResponseRedirect,HttpResponse
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
            return HttpResponseRedirect(request.GET.get('next') or '/bbs')#登录后，返回到提交前的页面
        else:
            login_err = 'Wrong username or password!'
            return render(request,'bbs/html/login.html',{'login_err':login_err})

    return  render(request,'bbs/html/login.html')

def acc_logout(request):
    logout(request)
    return  HttpResponseRedirect('/bbs')

def article_detail(request,article_id):
    article_obj = models.Article.objects.get(id=article_id)

    return render(request,'bbs/html/article_detail.html',{'article_obj':article_obj,
                                                          'category_list': category_list,})

def comment(request):
    print(request.POST)
    if request.method =='POST':
        new_comment_obj=models.Comment(
            article_id= request.POST.get('article_id'),
            parent_comment_id = request.POST.get('parent_comment_id') or None,
            comment_type = request.POST.get('comment_type'),
            user_id = request.user.userprofile.id,
            comment = request.POST.get('comment')
        )
        new_comment_obj.save()

        return HttpResponse('post-comment-success')
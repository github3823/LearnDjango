from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from bbs import models
from django.contrib.auth import login,logout,authenticate #用户验证相关
from django.contrib.auth.decorators import login_required
from bbs import comment_hander
from bbs import form
import json
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
    comment_tree = comment_hander.build_tree(article_obj.comment_set.select_related())


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

def get_comments(request,article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree =  comment_hander.build_tree(article_obj.comment_set.select_related())
    tree_html = comment_hander.render_comment_tree(comment_tree)
    return  HttpResponse(tree_html)

#@login_required#(login_url='指定url')第一种方法，指定登录跳转位置
@login_required()#直接setting里写LOGIN_URL=指定
def new_article(request):#发贴功能
    if request.method == "GET":
        article_form = form.ArticleModelForm()
        return  render(request,'bbs/html/new_article.html',{'article_form':article_form})
    elif request.method =="POST":
        print(request.POST)
        print(request.FILES)
        article_form = form.ArticleModelForm(request.POST,request.FILES)#文件和图片在FILES参数里
        if article_form.is_valid():
            data = article_form.cleaned_data
            data['author_id'] = request.user.userprofile.id
            article_obj = models.Article(**data)
            article_obj.save()
            #article_form.save()
            return HttpResponse('发布成功')
        else:
            return render(request, 'bbs/html/new_article.html', {'article_form': article_form})

def file_upload(request):#文件上传
    print(request.FILES.get('filename'))
    file_obj = request.FILES.get('filename')
    with open('templates/bbs/html/upload/%s' %file_obj.name, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return render(request, 'bbs/html/new_article.html')

def get_latest_article_count(request):#获取更新文章数量
    latest_article_id = request.GET.get("latest_id")
    print("前端传的",latest_article_id)
    if latest_article_id:
        new_article_count = models.Article.objects.filter(id__gt = latest_article_id).count()
        print("new article count",new_article_count)
    else:
        new_article_count=0
    return HttpResponse(json.dumps({'new_article_count':new_article_count}))


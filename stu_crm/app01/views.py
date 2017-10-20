from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import authenticate,login,logout#可以匹配admin user中的用户信息
# Create your views here.
@login_required
def index(request):
    return  render(request,'app01/index.html')


def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request,user)#登录用户
            return HttpResponseRedirect('/')
        else:
            login_err = 'Wrong username or password!'
            return render(request,'app01/login.html',{'login_err':login_err})

    return  render(request,'app01/login.html')

def acc_logout(request):
    logout(request)
    return  HttpResponseRedirect('/')
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse

class MyCustomMidelWare(MiddlewareMixin):
    # def __init__(self, get_response):
    #     print("--------in process response---")
    #     self.get_response = get_response
    #
    # def __call__(self, request):
    #     print("-----in process request--")
    #     return self.get_response(request)


    def process_request(self,request):#est提交给views之前
        print("-----in process request--")

        if request.user.username == 'shaopao':
            print("--no permission--")
            return HttpResponse("shaopao is no permission")

    def process_view(self,request,view_func,view_ares,veiw_kwargs):
        print("-----in process view--")
        print(request,view_func,view_ares,veiw_kwargs)


    def process_response(self,request, response):#返回浏览器前
        print("----in process response--")
        return  response
    #https://docs.djangoproject.com/en/1.9/topics/http/middleware/
    #返回浏览器之前有还可以定义其它两个

    def process_exception(self,request, exception):
        print("-------come to exception---")
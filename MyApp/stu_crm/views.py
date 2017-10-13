from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,'stu_crm/crm/dashboard.html')
from django.shortcuts import render,HttpResponse
from app01 import models
# Create your views here.
def index(request):
    return render(request,'app01/index.html')
def pay_py_cash(request):
    return HttpResponse('I use cash pay')
def page1(request):
    return render(request,'app01/page1.html')
def page1_1(request):
    return render(request,'app01/page1_1.html')
def book(request):
    if request.method == 'POST':
        print(request.POST)
        book_name = request.POST.get('name')
        publisher_id = request.POST.get('publisher_id')
        print('==>',request.POST.get('author_ids'))
        author_ids = request.POST.getlist('author_ids')

        print(book_name,publisher_id,author_ids)
        new_book = models.Book(
            name = book_name,
            publisher_id =publisher_id,
            publish_date = '2017-09-28'

        )
        new_book.save()
        new_book.authors.add(*author_ids)

    books =models.Book.objects.all()
    publisher_list = models.Publisher.objects.all()
    author_list = models.Athor.objects.all()

    return  render(request,'app01/book.html',{'books':books,
                                              'publishers':publisher_list,
                                              'authors':author_list,
                                              })
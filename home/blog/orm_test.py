import os
os.environ['DJANGO_SETTINGS_MODULE'] ='home.settings'
import  django
django.setup()

from blog import  models
from django.db.models import F
from django.db.models import Avg,Sum,Min,Count
from app01 import models as adb
# entry = models.Entry.objects.get(pk=1)
# tech_blog = models.Blog.objects.get(name='新手村屠杀高级选手指南')
#
# entry.blog = tech_blog
# entry.save()
# print(entry,tech_blog)
#obj = models.Entry.objects.filter(n_comments__lte=F('n_pingbacks'))
#select n_commnets,n_pingbacks from Entry where n_comments<n_pingbacks;
#print(obj)

#models.Entry.objects.update(n_pingbacks=F('n_pingbacks')+1)

#print(models.Entry.objects.all().aggregate(Avg('n_pingbacks'),Sum('n_pingbacks'),Min('n_pingbacks')))

#
# obj = adb.Publisher.objects.last()
# print(obj.name,obj.book_set.select_related())
print(adb.Book.objects.values_list('publish_date').annotate(Count('publish_date')))
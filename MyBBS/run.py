import os
os.environ['DJANGO_SETTINGS_MODULE'] ='MyBBS.settings'
import  django
django.setup()
from bbs import models
from django.db.models import Avg,Sum,Min,Count
obj=models.Article.objects.filter(status='published')

for article in obj:

    aa=article.comment_set.select_related()
    print(aa)

print(obj)
from django.db import models

# Create your models here.
class Athor(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    def __str__(self):
        return "<%s %s>" %(self.first_name,self.last_name)
    class Meta:#admin后台显示别名
        verbose_name_plural = '作者'

class Publisher(models.Model):
    name = models.CharField(max_length=64,unique=True)#唯一
    address = models.CharField(max_length=128,null=True,blank=True)#此行值可为空
    city = models.CharField(max_length=64)
    state_province = models.CharField(max_length=30,verbose_name='所属省',help_text='所在国家省份')#admin后面显示提示信息和别名
    country = models.CharField(max_length=50,editable=False)#此行admin后台不显示
    website = models.URLField()
    def __str__(self):
        return "<%s>"  %(self.name)
    class Meta:
        verbose_name_plural = '出版社'
class Book(models.Model):
    name = models.CharField(max_length=128)
    authors = models.ManyToManyField(Athor)
    publisher = models.ForeignKey(Publisher)
    publish_date = models.DateField()
    def __str__(self):
        return "<%s>" % (self.name)
    class Meta:
        verbose_name_plural = '书名'
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
# Create your models here.
class Article(models.Model):#帖子内容
    title = models.CharField(max_length=255)#标题
    brief = models.CharField(max_length=255,blank=True,null=True)#简介
    category = models.ForeignKey('Category')#帖子关联所属板块，Category在下面，可以用引号括起来，反射到字段
    content = models.TextField("文章内容")
    author = models.ForeignKey('UserProfile')#作者
    pub_date = models.DateTimeField(blank=True,null=True)#记录创建时间
    last_modify= models.DateTimeField(auto_now=True)#修改时间
    priority = models.IntegerField('优先级',default=1000)
    head_img = models.ImageField('标题图片',upload_to='templates/bbs/html/upload')#头像
    status_choices = (('draft','草稿'),
                      ('published','已发布'),
                      ('hidden','隐藏'),)
    status = models.CharField(choices=status_choices,default='published',max_length=64)

    def __str__(self):
        return self.title

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError(('Draft entries may not have a publication date.'))
        # Set the pub_date for published items if it hasn't been set already.
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()


class Comment(models.Model):#帖子评论
    article = models.ForeignKey(Article,verbose_name='')#所属文章
    parent_comment = models.ForeignKey('self',related_name='my_children',blank=True,null=True)
    comment_choices = ((1,'评论'),
                       (2,'点赞'),)
    comment_type = models.IntegerField(choices=comment_choices,default=1)#评论类型
    user = models.ForeignKey('UserProfile')#谁的评论
    comment = models.TextField(blank=True,null=True)#评论内容
    date = models.DateTimeField(auto_now_add=True)  # 评论时间

    def clean(self):
        if self.comment_type == 1 and len(self.comment) == 0:#选择评论且内容为空
            raise ValidationError('评论内容不能为空，二五')
    def __str__(self):
        return '%s,P:%s,%s' %(self.article,self.parent_comment,self.comment)

class Category(models.Model):#板块
    name = models.CharField(max_length=64,unique=True)#板块名
    brief = models.CharField(null=True,blank=True,max_length=255)#简介
    set_as_top_menu =models.BooleanField(default=False)#位置
    position_index = models.SmallIntegerField()#展示位置
    admins = models.ManyToManyField('UserProfile',blank=True)#版主
    def __str__(self):
        return self.name

class UserProfile(models.Model):#用户
    user = models.OneToOneField(User)#使用django创建管理员用户
    name = models.CharField(max_length=32)#名字
    signature = models.CharField(max_length=255,blank=True,null=True)#签名
    head_img = models.ImageField(height_field=150,width_field=150,blank=True,null=True)#头像

    def __str__(self):
        return self.name
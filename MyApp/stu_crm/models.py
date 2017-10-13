from django.db import models
# Create your models here.
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User #导入django用户表

course_type_choices = (('online', u'网络班'),
                          ('offline_weekend', u'面授班(周末)',),
                          ('offline_fulltime', u'面授班(脱产)',),
                          )#以什么形式上课选项


class School(models.Model):#创建学校表
    name = models.CharField(max_length=128,unique=True)#学校名，不能重名
    city = models.CharField(max_length=64)#学校所在城市
    addr = models.CharField(max_length=128)#学校所在地址
    def __str__(self):
        return self.name#反射字段名
class UserProfile(models.Model):#创建用户表
    user = models.OneToOneField(User)#一对一 关联到django用户表
    name = models.CharField(max_length=64)
    school = models.ForeignKey('School')#关联School表
    def __str__(self):
        return self.name  # 反射字段名
class Customer(models.Model):#创建客户表
    qq = models.CharField(max_length=64,unique=True)
    name = models.CharField(max_length=32,blank=True,null=True)#客户资询字段名字不是必要的
    ptone = models.BigIntegerField(blank=True,null=True)#电话，长整数
    course = models.ForeignKey('Course')#要咨询的课程，关联课程表

    course_type = models.CharField(max_length=64,choices=course_type_choices,default='offline_weekend')#要以什么形式上课
    consult_memo = models.TextField()#咨询记录
    source_type_choices = (('qq', u"qq群"),
                   ('referral', u"内部转介绍"),
                   ('51cto', u"51cto"),
                   ('agent', u"招生代理"),
                   ('others', u"其它"),
                   )#来源渠道选项
    source_type = models.CharField(max_length=64,choices=source_type_choices)#来源渠道
    referral_from = models.ForeignKey('self',blank=True,null=True,related_name="internal_who")#写表名也行'Customer',关联自己
    status_choices = (('signed',u"已报名"),
                      ('unregistered',u"未报名"),
                      ('graduated',u"已毕业"),
                      ('drop-off',u"退学"),
                      )#客户状态
    status = models.CharField(choices=status_choices,max_length=64)#记录客户状态
    consultant = models.ForeignKey('UserProfile',verbose_name='课程顾问')#记录接待人
    class_list = models.ManyToManyField("ClassList",blank=True)#manytomany不需要null=True,记录已报名客户所在班级
    date = models.DateField('咨询日期',auto_now_add=True)#记录咨询日期

    def __str__(self):
        return "%s(%s)" %(self.qq,self.name)
class CustomerTrackRecord(models.Model):#客户跟踪
    customer = models.ForeignKey(Customer)#关联客户
    track_record    =   models.TextField("跟踪记录")
    track_date = models.DateField(auto_now_add=True)#日期
    follower = models.ForeignKey(UserProfile)
    status_choices = ((1, u"近期无报名计划"),
                      (2, u"2个月内报名"),
                      (3, u"1个月内报名"),
                      (4, u"2周内报名"),
                      (5, u"1周内报名"),
                      (6, u"2天内报名"),
                      (7, u"已报名"),
                      )
    status = models.IntegerField(u"状态", choices=status_choices, help_text=u"选择客户此时的状态")
    def __str__(self):
        return self.customer

class Course(models.Model):#课程表
    name = models.CharField(max_length=64,unique=True)#课程名
    online_price = models.IntegerField()#网络班价格
    offline_price = models.IntegerField()#面授班价格
    introduction = models.TextField()#课程介绍
    def __str__(self):
        return self.name
class ClassList(models.Model):#班级表
    couerse = models.ForeignKey(Course,verbose_name="课程")#关联课程
    semester = models.IntegerField(verbose_name="学期")#学期
    course_type = models.CharField(max_length=64,choices=course_type_choices,default='offline_weekend')#要以什么形式上课
    teachers = models.ManyToManyField(UserProfile)#授课老师
    start_date = models.DateField()#开班日期
    graudate_date = models.DateField()#毕业日期
    def __str__(self):
        return  "%s(%s)(%s)" %(self.couerse.name,self.course_type,self.semester)
    class Meta:
        unique_together = ('couerse','semester','course_type')#联合唯一
class CourseRecord(models.Model):#课程记录
    class_obj = models.ForeignKey(ClassList)
    day_num = models.IntegerField('第几节课')
    course_date = models.DateField(auto_now_add=True,verbose_name='课程日期')
    teacher = models.ForeignKey(UserProfile)#带课老师

    def __str__(self):
        return "%s,%s" %(self.class_obj,self.day_num)
    class Meta:
        unique_together = ('class_obj','day_num')
class StudyRecord(models.Model):
    course_record = models.ForeignKey(CourseRecord)
    student = models.ForeignKey(Customer)
    record_choices = (('checked', u"已签到"),
                      ('late', u"迟到"),
                      ('noshow', u"缺勤"),
                      ('leave_early', u"早退"),
                      )
    record = models.CharField(u"状态", choices=record_choices, default="checked", max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, 'D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField(u"本节成绩", choices=score_choices, default=-1)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(u"备注", max_length=255, blank=True, null=True)#记录特殊情况

    def __str__(self):
        return "%s,%s,%s" %(self.course_record,self.student,self.record)


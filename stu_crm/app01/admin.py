from django.contrib import admin

# Register your models here.
from app01 import models as app01




admin.site.register(app01.Customer)
admin.site.register(app01.ConsultRecord)
admin.site.register(app01.ClassList)
admin.site.register(app01.CourseRecord)
admin.site.register(app01.StudyRecord)
admin.site.register(app01.UserProfile)
admin.site.register(app01.Course)
admin.site.register(app01.School)
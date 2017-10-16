from  django.forms import Form,ModelForm
from stu_crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude =()
    def __init__(self,*args,**kwargs):
        super(CustomerModelForm,self).__init__(*args,**kwargs)#先继承下，再重写

        for field_name in self.base_fields:#循环所有子项,批量添加样式
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})

from django.forms import ModelForm
from bbs import models



class ArticleModelForm(ModelForm):
    class Meta:
        model = models.Article
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ArticleModelForm, self).__init__(*args, **kwargs)  # 先继承下，再重写

        for field_name in self.base_fields:  # 循环所有子项,批量添加样式
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})
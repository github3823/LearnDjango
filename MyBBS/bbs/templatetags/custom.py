from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html#将数据转为html代码

register = template.Library()



@register.filter
def truncate_url(img_url):
    # print(img_url.url,img_url.name)
    # print(img_url.url.split('/')[-1])
    return img_url.url.split('/')[-1]

@register.simple_tag
def filter_comment(article_obj):
    quety_set = article_obj.comment_set.select_related()
    comments = {
        'comment_count':quety_set.filter(comment_type=1).count(),
        'thumb_count':quety_set.filter(comment_type=2).count(),
    }
    return comments
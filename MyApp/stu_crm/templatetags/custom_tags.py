from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html#将数据转为html代码

register = template.Library()

@register.filter
@stringfilter
def self_upper(value):
    print("--val from template--",value)
    return value.upper()

@register.simple_tag# 可传参数前端使用 {% guess_page customer_list.number page_num %}
def guess_page(current_page,loop_num):
        # { % if page_num == customer_list.number %}
        # < li class ="active" > < a href="?page={{ page_num }}" > {{page_num}} < / a > < / li >
        # { % else %}
        # < li class ="" > < a href="?page={{ page_num }}" > {{page_num}} < / a > < / li >
        # { % endif %}
    offset = abs(current_page-loop_num)
    if offset <3:
        if current_page == loop_num:
            page_ele = """<li class ="active"><a href="?page=%s"> %s </a></li>"""  %(loop_num,loop_num)
        else:
            page_ele = """<li class =""><a href="?page=%s"> %s </a></li>"""  %(loop_num,loop_num)
        return format_html(page_ele,)
    else:
        return ''
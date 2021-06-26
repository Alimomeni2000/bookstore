from django import template
from ..models import Category
register = template.Library()

@register.inclusion_tag("navbar.html")
def navbar():
    
    return {
        "category": Category.objects.all(),
        
    }
@register.inclusion_tag("registration/partials/link.html")
def link(request,link_name,content):
    return {
        "request":request,
        "link_name":link_name,
        "link":"account:{}".format(link_name),
        "content":content,

    }
from django import template
from ..models import Category
register = template.Library()

@register.inclusion_tag("navbar.html")
def navbar():
    
    return {
        "category": Category.objects.all(),
        
    }

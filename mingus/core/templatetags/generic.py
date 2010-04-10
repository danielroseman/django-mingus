from efficient import utils
from django.template import Library

register = Library()


@register.simple_tag
def get_proxies_and_comments(queryset):
    utils.get_generic_relations(queryset)
    actual_qs = [obj.content_object for obj in queryset]
    utils.get_generic_related_objects(actual_qs, 'comments')
    for obj in queryset:
        obj.comment_count = len(obj.content_object.comments)
    return ''

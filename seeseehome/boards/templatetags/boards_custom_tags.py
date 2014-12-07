from django import template
from boards.models import *

register = template.Library()
@register.filter
def num_of_comments_in_post(post):
#    post = Post.objects.get_post(post_id)
    num_of_comments_in_post = Comment.objects.filter(post=post).count()
    return num_of_comments_in_post


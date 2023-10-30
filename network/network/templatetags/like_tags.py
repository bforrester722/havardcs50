from django import template

from network.models import Like
register = template.Library()

@register.filter(name="has_liked")

# check if user has liked a post for defaulting heart icon 
def has_liked(user, post):
    if not user.is_authenticated:
        return False

    return Like.objects.filter(user=user, post=post).exists()

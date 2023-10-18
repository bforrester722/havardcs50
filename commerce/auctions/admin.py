from django.contrib import admin
from .models import Listing, Comment, User, Bid

# Register your models here.

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(User)

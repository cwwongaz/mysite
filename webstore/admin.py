from django.contrib import admin
from .models import User, client, comment, item, rating

# Register your models here.
admin.site.register(User)
admin.site.register(client)
admin.site.register(comment)
admin.site.register(item)
admin.site.register(rating)
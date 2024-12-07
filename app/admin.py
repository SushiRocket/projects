from django.contrib import admin
from .models import Profile, Tweet, Like

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avator')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tweet)
admin.site.register(Like)

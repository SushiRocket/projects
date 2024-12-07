from django.contrib import admin
from .models import Profile, Tweet, Like, User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(User)
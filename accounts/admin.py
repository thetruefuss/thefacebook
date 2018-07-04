from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
    date_hierarchy = 'created'
admin.site.register(Profile, ProfileAdmin)  # noqa: E305

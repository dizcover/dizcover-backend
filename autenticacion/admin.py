from django.contrib import admin
from .models import Users

# Register your models here.
admin.site.register(Users)

# @admin.register(SocialToken)
# class SocialTokenAdmin(admin.ModelAdmin):
#     list_display = ('account', 'token', 'expires_at')
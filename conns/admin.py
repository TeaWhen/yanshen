from django.contrib import admin
from conns.models import AuthInfo

class AuthInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuthInfo, AuthInfoAdmin)

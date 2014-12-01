from django.contrib import admin
from users.models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    exclude = ('password', 'username', 'email', 
                'last_login',)

admin.site.register(User, UserAdmin)


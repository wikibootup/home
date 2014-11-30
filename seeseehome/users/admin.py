from django.contrib import admin
from users.models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ('password', 'username', 'email', 
                'last_login',)

admin.site.register(User, UserAdmin)



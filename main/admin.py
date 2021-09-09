from django.contrib import admin
from .models import AdvUser, Order


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ( 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))

    readonly_fields = ('last_login', 'date_joined')


admin.site.register(Order)

admin.site.register(AdvUser, AdvUserAdmin)
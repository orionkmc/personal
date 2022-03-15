from django.contrib import admin
from apps.locals.models import Local, Manager, Employee


class ManagerInline(admin.TabularInline):
    model = Manager
    extra = 0
    raw_id_fields = ('manager', )


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0
    raw_id_fields = ('employee', )


class LocalAdmin(admin.ModelAdmin):
    inlines = [ManagerInline, EmployeeInline]
    raw_id_fields = ('owner', )
    list_display = ('admin_thumbnail', 'name', 'phone', )


admin.site.register(Local, LocalAdmin)
admin.site.register(Manager)
admin.site.register(Employee)

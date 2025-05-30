from django.contrib import admin

from apps.models import DebtBook


@admin.register(DebtBook)
class DebtBookAdmin(admin.ModelAdmin):
    list_display = 'id','name','number'


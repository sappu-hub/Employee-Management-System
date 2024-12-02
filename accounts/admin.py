from django.contrib import admin
from .models import DynamicForm

@admin.register(DynamicForm)
class DynamicFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'configuration')  # Display name and configuration in the admin

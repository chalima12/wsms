from django.contrib import admin
from .models import *
fname='first_name'
class UsersAdmin(admin.ModelAdmin):
    search_fields=['first_name','last_name','user_type']
    list_display=['user_id',fname,'last_name','user_name','user_type','is_active']
    list_editable=['first_name','last_name']
    list_filter=['user_type']
# Register your models here.
admin.site.register(Users,UsersAdmin)
admin.site.register(Item)
admin.site.register(Assignments)
admin.site.register(Section)
admin.site.register(Component)
# admin.site.register(Work_with)

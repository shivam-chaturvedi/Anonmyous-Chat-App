from django.contrib import admin
from chat.models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display=('id','name')
admin.site.register(Member,MemberAdmin)

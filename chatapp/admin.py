from django.contrib import admin
from ChatApp.models import Member,Groups

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display=('id','Name','Group')
admin.site.register(Member,MemberAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display=('id','Name','Limit')

admin.site.register(Groups,GroupAdmin)
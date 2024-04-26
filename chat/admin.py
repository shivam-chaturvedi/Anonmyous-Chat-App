from django.contrib import admin
from chat.models import Member,Groups

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display=('id','Name','Group')
admin.site.register(Member,MemberAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display=('id','Name')

admin.site.register(Groups,GroupAdmin)
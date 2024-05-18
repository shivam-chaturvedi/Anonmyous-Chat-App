from django.shortcuts import render
from django.http import JsonResponse
from ChatApp.models import *
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def home(req):
    if(req.method=="POST"):
        try:
            json_data=json.loads(req.body.decode('utf-8'))
            username=json_data.get('username')
            if(json_data.get("createGroup")):
                group_name=json_data.get('groupName')
                group_limit=int(json_data.get('groupLimit'))
                Group=Groups.objects.create(Name=group_name,Limit=group_limit)
                member=Member.objects.create(Name=username,Group=Group,Role="admin")
                return JsonResponse({'memberid':member.id},status=200)
            else:
                group_id=json_data.get("groupId")
                group=Groups.objects.get(id=group_id)
                current_group_members=group.member_set.all().__len__()
                print(current_group_members)
                if(current_group_members>=group.Limit):
                    return JsonResponse({'error':"The group has already reached its maximum number of members"},status=400)
                member=Member.objects.create(Name=username,Group=group)
                return JsonResponse({'memberid':member.id},status=200)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
    else:
        return render(req,'index.html')
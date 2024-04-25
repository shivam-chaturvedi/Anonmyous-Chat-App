from django.shortcuts import render
from django.http import HttpResponse
from chat.models import Member

# Create your views here.
def home(req):
    if(req.method=="POST"):
        print(req.POST)
        name=req.POST.get('username')
        obj=Member.objects.create(name=name)
        id=obj.id
        obj.save()
        return render(req,'chat-room.html',{'userid':id})
    else:
        return render(req,'index.html')
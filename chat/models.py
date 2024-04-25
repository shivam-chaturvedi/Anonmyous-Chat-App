from django.db import models

# Create your models here.

class Groups(models.Model):
    # GroupId=models.CharField(max_length=20,primary_key=True)
    Name=models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.Name


class Member(models.Model):
    Name=models.CharField(max_length=100)
    Group=models.ForeignKey(Groups,on_delete=models.CASCADE)
    ChannelName=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.Name
    




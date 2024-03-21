import uuid
from django.db import models
from user.models import User

class Post(models.Model):
    post_id= models.UUIDField(primary_key= True, editable= False, default= uuid.uuid4)
    post_title= models.CharField(max_length=255)
    post_description= models.CharField(max_length=255)
    created_on= models.DateField()
    modified_on= models.DateField(null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to="my_picture",blank=True)
    
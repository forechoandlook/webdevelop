from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
# Create your models here.

class Comment(model.Model):

	belong_article = model.ForeignKey()
	belong_user = model.ForeignKey(User,relate_name="user")
	parent_comment = model.ForeignKey()
	content = model.ChairField(max_length=200,null=False)
	create = model.DateTimeField(null=False,default = now)


	def __str__(self):
		return self.belong_user.username+":"+self.content
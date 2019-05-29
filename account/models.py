from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birth = models.DateField(verbose_name='生日',blank=True, null=True)
    phone = models.CharField(verbose_name='电化号码',max_length=20, null=True)

    class Meta:
        db_table = "UserProfile"
        verbose_name_plural = u'用户描述'

    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    school = models.CharField(verbose_name='学校',max_length=100, blank=True)
    company = models.CharField(verbose_name='公司',max_length=100, blank=True)
    profession = models.CharField(verbose_name='职业',max_length=100, blank=True)
    address = models.CharField(verbose_name='地址',max_length=100, blank=True)
    aboutme = models.TextField(verbose_name='详细内容',blank=True)
    photo = models.ImageField(verbose_name='图片',blank=True,upload_to="profile/")

    class Meta:
        db_table='用户信息'
    def __str__(self):
        return "user:{}".format(self.user.username)

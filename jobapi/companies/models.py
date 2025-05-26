from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    #
    # ROLE_CHOICES = (
    #     ('admin', 'Admin'),
    #     ('user', 'User'),
    #     ('candidate', 'Candidate'),
    # )
    # role = models.CharField(choices=ROLE_CHOICES, max_length=20)
    # #


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Company(BaseModel):
    #
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    #
    name = models.CharField(max_length=255)
    description = models.TextField()
    tax_code = models.CharField(max_length=50)
    image = CloudinaryField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class Job(BaseModel):
    name = models.CharField(max_length=255)
    title = RichTextField()
    salary = models.IntegerField()
    address = models.TextField()
    image = CloudinaryField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    #
    # content = models.TextField()
    # author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='jobs')
    #


    class Meta:
        unique_together = ('name', 'company')

    def __str__(self):
            return self.name

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


#
# class Post(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title









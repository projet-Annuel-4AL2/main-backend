from django.db import models


class Groupe(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    author = models.ForeignKey('userApi.CustomUser', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField('userApi.CustomUser', related_name='group_members', blank=True)
    admin = models.ForeignKey('userApi.CustomUser', related_name='group_admin', on_delete=models.CASCADE , null=True, blank=True)
    group_pic = models.ImageField(upload_to='group_pics/', null=True, blank=True)

    
class GroupePublication(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    author = models.ForeignKey('userApi.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('userApi.CustomUser', related_name='publication_likes', blank=True)
    comments = models.ManyToManyField('userApi.CustomUser', related_name='publication_comments', blank=True)
    image = models.ImageField(upload_to='publication_pics/', null=True, blank=True)

class CommentPublication(models.Model):
    publication = models.ForeignKey(GroupePublication, on_delete=models.CASCADE, related_name='publication')
    author = models.ForeignKey('userApi.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
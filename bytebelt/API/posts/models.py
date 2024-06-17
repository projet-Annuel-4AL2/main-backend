from django.db import models



class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('userApi.CustomUser', on_delete=models.CASCADE)
    likes = models.ManyToManyField('userApi.CustomUser', related_name='likes', symmetrical=False)
    dislikes = models.ManyToManyField('userApi.CustomUser', related_name='dislikes', symmetrical=False)
    comments = models.ManyToManyField('userApi.CustomUser', related_name='comments', symmetrical=False)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    document = models.FileField(upload_to='posts/', null=True, blank=True)
    tags = models.CharField(max_length=100 , null=True, blank=True)
    category = models.CharField(max_length=100 , null=True, blank=True)

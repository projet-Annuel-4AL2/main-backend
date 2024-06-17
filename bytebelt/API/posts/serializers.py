from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Posts

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'title', 'content', 'user', 'image', 'document', 'tags', 'category']

    def create(self, validated_data):
        response = requests.get(API_BASE_URL + 'getuserbytoken/')
        user_id = response.json().get('id')
        user = get_object_or_404(User, pk=user_id) 
        post = Posts.objects.create(user=user, **validated_data)
        return post
        
        
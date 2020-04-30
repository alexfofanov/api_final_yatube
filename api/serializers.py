from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only='True')

    class Meta:
        fields = '__all__'
        read_only_fields = ('pub_date',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only='True')
    
    class Meta:
        fields = '__all__'
        read_only_fields = ('created',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title')
        model = Group     


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only='True')
    following = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow    

    def validate_following(self, value):
        filter_by_user = Follow.objects.filter(user=self.context['request'].user, following__username=value)
        if filter_by_user.exists():   
            raise serializers.ValidationError('Вы уже продписаны на этого пользователя.')
        return value
        

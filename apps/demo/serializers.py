from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['text', 'timestamp', 'username']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.SerializerMethodField()
    latest_comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'username', 'comment_count', 'latest_comments']
    
    def get_comment_count(self, post_instance):
        return post_instance.comments.count()
    
    def get_latest_comments(self, post_instance):
        recent_comments = post_instance.comments.all()[:3]  
        return CommentSerializer(recent_comments, many=True).data
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db import models
from .models import Post
from .serializers import PostSerializer
from .models import Comment


class PostPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 50


class PostListView(generics.ListAPIView):
    """
    API endpoint for infinite scrolling list of posts.
    
    Returns posts ordered by timestamp (latest first), with up to 3 latest comments per post.
    
    Usage:
    GET /api/posts/
    GET /api/posts/?page=2
    GET /api/posts/?page_size=20
    
    Response format:
    {
        "count": 100,
        "next": "http://localhost:8000/api/posts/?page=2",
        "previous": null,
        "results": [
            {
                "id": "uuid-here",
                "text": "Post content",
                "timestamp": "2024-01-01T12:00:00Z",
                "username": "author_username",
                "comment_count": 5,
                "latest_comments": [
                    {
                        "text": "Comment text",
                        "timestamp": "2024-01-01T12:05:00Z",
                        "username": "commenter_username"
                    }
                ]
            }
        ]
    }
    """
    serializer_class = PostSerializer
    pagination_class = PostPagination
    
    def get_queryset(self):
        return Post.objects.select_related('user').prefetch_related(
            models.Prefetch(
                'comments',
                queryset=Comment.objects.select_related('user').order_by('-timestamp')
            )
        ).order_by('-timestamp')


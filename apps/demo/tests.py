from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post, Comment
from django.urls import reverse


class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        
        self.post1 = Post.objects.create(text="First post", user=self.user)
        self.post2 = Post.objects.create(text="Second post", user=self.user)
        
        Comment.objects.create(text="Comment 1", post=self.post1, user=self.user)
        Comment.objects.create(text="Comment 2", post=self.post1, user=self.user)
        Comment.objects.create(text="Comment 3", post=self.post1, user=self.user)
        Comment.objects.create(text="Comment 4", post=self.post1, user=self.user)
        
        Comment.objects.create(text="Post2 comment", post=self.post2, user=self.user)
    
    def test_posts_list_endpoint(self):
        """Test that the endpoint returns posts with pagination"""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertEqual(len(data['results']), 2)  
    
    def test_posts_ordered_by_timestamp(self):
        """Test posts are ordered latest first"""
        response = self.client.get('/api/posts/')
        data = response.json()
        
        posts = data['results']
        self.assertEqual(posts[0]['text'], "Second post")
        self.assertEqual(posts[1]['text'], "First post")
    
    def test_comment_count_accuracy(self):
        """Test that comment_count reflects actual comment count"""
        response = self.client.get('/api/posts/')
        data = response.json()
        
        post1_data = next(p for p in data['results'] if p['text'] == "First post")
        self.assertEqual(post1_data['comment_count'], 4)
    
    def test_latest_comments_limit(self):
        """Test that only 3 latest comments are returned per post"""
        response = self.client.get('/api/posts/')
        data = response.json()
        
        post1_data = next(p for p in data['results'] if p['text'] == "First post")
        self.assertEqual(len(post1_data['latest_comments']), 3)
        
        post2_data = next(p for p in data['results'] if p['text'] == "Second post")
        self.assertEqual(len(post2_data['latest_comments']), 1)
    
    def test_required_fields_present(self):
        """Test that all required fields are present in response"""
        response = self.client.get('/api/posts/')
        data = response.json()
        
        post = data['results'][0]
        required_fields = ['id', 'text', 'timestamp', 'username', 'comment_count', 'latest_comments']
        
        for field in required_fields:
            self.assertIn(field, post)
        
        if post['latest_comments']:
            comment = post['latest_comments'][0]
            comment_fields = ['text', 'timestamp', 'username']
            for field in comment_fields:
                self.assertIn(field, comment)
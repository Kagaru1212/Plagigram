from django.test import TestCase, Client
from django.urls import reverse

from insta.models import Post, TagPost, Comment, Like
from plagigram import settings
from users.models import User


class TestInsta(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='Test Content')

        self.tag = TagPost.objects.create(tag='testtag')
        self.post1 = Post.objects.create(user=self.user, title='Post 1', text='Content 1')
        self.post2 = Post.objects.create(user=self.user, title='Post 2', text='Content 2')
        self.post1.tags.add(self.tag)
        self.post2.tags.add(self.tag)

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        response = self.client.get(reverse('addpost'))
        self.assertEqual(response.status_code, 200)

    def test_post_comments(self):
        post = Post.objects.create(user=self.user)
        response = self.client.get(reverse('comments', args=[post.id]))

        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        comment_text = 'Test Comment'
        form_data = {'text': comment_text}
        response = self.client.post(reverse('add_comment', args=[self.post.id]), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(post=self.post, user=self.user, text=comment_text).exists())

    def test_like_post(self):
        response = self.client.post(reverse('like_post', args=[self.post.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('like_post', args=[self.post.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_posts_by_tag(self):
        response = self.client.get(reverse('posts_by_tag', args=['testtag']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tag'], self.tag)
        self.assertIn(self.post1, response.context['posts'])
        self.assertIn(self.post2, response.context['posts'])

    def test_posts_by_nonexistent_tag(self):
        # Trying to get posts with a tag that doesn't exist
        response = self.client.get(reverse('posts_by_tag', args=['nonexistenttag']))

        self.assertEqual(response.status_code, 404)


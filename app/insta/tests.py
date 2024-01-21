"""
This is a file with tests for insta application in it there is a class with tests for each viewport.

The setUp function will occur in each test class,
it contains all actions that will take place before the start of each test in the class.
"""
from django.test import TestCase, Client
from django.urls import reverse

from insta import views
from insta.models import Post, TagPost, Comment, Like
from users.models import User


class IndexViewTest(TestCase):
    """This is the class for the (index) view tests."""

    def setUp(self):
        """This function creates and registers a user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_index(self):
        """This test verifies that the home page exists and has a code of 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_correct_template(self):
        """This test verifies that the home page is using the correct template for display."""
        response = self.client.get('/plagigram/')
        self.assertTemplateUsed(response, 'insta/index.html')


class AddPostViewTest(TestCase):
    """This is the class for the (add_post) view tests."""

    def setUp(self):
        """This function creates and registers a user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_post(self):
        """This test verifies that the post creation page exists and has a code of 200."""
        response = self.client.get(reverse('addpost'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_view_correct_template(self):
        """This test verifies that the post creation page is using the correct template for display."""
        response = self.client.get('/plagigram/addpost/')
        self.assertTemplateUsed(response, 'insta/addpost.html')

    def test_add_post_view_renders_form(self):
        """This test checks if the correct forms are used when creating a page."""
        response = self.client.get('/plagigram/addpost/')
        self.assertIsInstance(response.context['form'], views.AddPostForm)
        self.assertIsInstance(response.context['image_formset'], views.PostUploadImageFormSet)


class CommentsViewTest(TestCase):
    """This is the class for the (post_comments) view tests."""

    def setUp(self):
        """This function creates and registers a user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        post = Post.objects.create(user=self.user)
        self.url = reverse('comments', args=[post.id])

    def test_post_comments(self):
        """This test checks the display of the post comments page and that its code is 200."""
        post = Post.objects.create(user=self.user)
        response = self.client.get(reverse('comments', args=[post.id]))

        self.assertEqual(response.status_code, 200)

    def test_post_comments_view_correct_template(self):
        """This test verifies that the comments page is using the correct template for display."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'insta/comments.html')

    def test_post_comments_view_renders_form(self):
        """This test checks if the correct forms are used when creating a page."""
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], views.CommentForm)


class AddCommentsViewTest(TestCase):
    """This is the class for the (add_comment) view tests."""

    def setUp(self):
        """This function creates and registers a user and also creates a post for that user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='Test Content')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_comment(self):
        """This function tests creating a comment for a post and adding it to the database."""
        comment_text = 'Test Comment'
        form_data = {'text': comment_text}
        response = self.client.post(reverse('add_comment', args=[self.post.id]), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(post=self.post, user=self.user, text=comment_text).exists())


class LikePostViewTest(TestCase):
    """This is the class for the (like_post) view tests."""

    def setUp(self):
        """This function creates and registers a user and also creates a post for that user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='Test Content')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_like_post(self):
        """This feature tests the addition of a like."""
        response = self.client.post(reverse('like_post', args=[self.post.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())

    def test_unlike_post(self):
        """This feature tests the deletion of a like."""
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('like_post', args=[self.post.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())


class TagPostViewTest(TestCase):
    """This is the class for the (posts_by_tag) view tests."""

    def setUp(self):
        """
        This function creates and registers a user,
        it also creates a tag. It then creates several posts for the user and connects them with tags.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = TagPost.objects.create(tag='testtag')
        self.post1 = Post.objects.create(user=self.user, title='Post 1', text='Content 1')
        self.post2 = Post.objects.create(user=self.user, title='Post 2', text='Content 2')
        self.post1.tags.add(self.tag)
        self.post2.tags.add(self.tag)

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_posts_by_tag(self):
        """This test checks if the posts associated with a certain tag are displayed correctly if they exist."""
        response = self.client.get(reverse('posts_by_tag', args=['testtag']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tag'], self.tag)
        self.assertIn(self.post1, response.context['posts'])
        self.assertIn(self.post2, response.context['posts'])

    def test_posts_by_nonexistent_tag(self):
        """This test verifies that a non-existent tag will result in a 404 code when accessed."""
        # Trying to get posts with a tag that doesn't exist
        response = self.client.get(reverse('posts_by_tag', args=['nonexistenttag']))

        self.assertEqual(response.status_code, 404)


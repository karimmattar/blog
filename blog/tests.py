"""
Blog tests cases
"""

from guardian.shortcuts import assign_perm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Profile, Comment

User = get_user_model()


class ProfileTest(TestCase):
    """
    Profile test cases
    """

    def setUp(self):
        """
        create user
        :return:
        """
        _user = User.objects.create_user(
            email="exist@test.local",
            username="exist_local",
            password="T@eST1926",
        )
        _permission = Permission.objects.filter(
            codename__in=[
                "view_profile",
                "add_profile",
                "change_profile",
                "delete_profile",
            ]
        ).values_list("id", flat=True)
        _user.user_permissions.add(*_permission)
        self.client = APIClient()

    @staticmethod
    def get_token(user):
        """
        get token
        :param user:
        :return:
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_profile_retrieve(self):
        """
        test retrieve profile
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        response = self.client.get(
            "/api/profile/", headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        """
        test update profile
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = self.client.patch(
            "/api/profile/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 200)


class PostTest(TestCase):
    """
    Post test cases
    """

    def setUp(self):
        """
        create user
        :return:
        """
        _user = User.objects.create_user(
            email="exist@test.local",
            username="exist_local",
            password="T@eST1926",
        )
        _user_2 = User.objects.create_user(
            email="exist_other@test.local",
            username="exist_other_local",
            password="T@eST1926",
        )
        _permission = Permission.objects.filter(
            codename__in=["view_post", "add_post", "change_post", "delete_post"]
        ).values_list("id", flat=True)
        _user.user_permissions.add(*_permission)
        _user_2.user_permissions.add(*_permission)
        self.client = APIClient()

    @staticmethod
    def get_token(user):
        """
        get token
        :param user:
        :return:
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def post_create(user):
        """
        post create
        :param user:
        :return:
        """
        _profile, _ = Profile.objects.get_or_create(bio="test", user=user)
        _post = Post.objects.create(title="test", content="test", author=_profile)
        return _post

    def test_post_create(self):
        """
        test create post
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _data = {
            "title": "test",
            "content": "test",
        }
        response = self.client.post(
            "/api/posts/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 201)

    def test_post_retrieve(self):
        """
        test create post
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _data = {
            "title": "test",
            "content": "test",
        }
        post = self.client.post(
            "/api/posts/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        response = self.client.get(
            f"/api/posts/{post.data['id']}/",
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_update(self):
        """
        test create post
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _data = {
            "title": "test",
            "content": "test",
        }
        post = self.client.post(
            "/api/posts/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        body = {
            "title": "test_update",
            "content": "test_update",
        }
        response = self.client.patch(
            f"/api/posts/{post.data['id']}/",
            body,
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        """
        test delete post
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _data = {
            "title": "test",
            "content": "test",
        }
        post = self.client.post(
            "/api/posts/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        response = self.client.delete(
            f"/api/posts/{post.data['id']}/",
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 204)

    def test_post_update_permission_denied(self):
        """
        test update post permission denied
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _user_2 = User.objects.get(email="exist_other@test.local")
        _token = self.get_token(_user_2)
        _post = self.post_create(_user)
        body = {
            "title": "test_update",
            "content": "test_update",
        }
        response = self.client.patch(
            f"/api/posts/{_post.id}/",
            body,
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 403)

    def test_post_delete_permission_denied(self):
        """
        test delete post permission denied
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _user_2 = User.objects.get(email="exist_other@test.local")
        _token = self.get_token(_user_2)
        _post = self.post_create(_user)
        response = self.client.delete(
            f"/api/posts/{_post.id}/", headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 403)

    def test_post_list(self):
        """
        test list post
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        response = self.client.get(
            f"/api/posts/", headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 200)


class CommentTest(TestCase):
    """
    Comment test cases
    """

    def setUp(self):
        """
        create user
        :return:
        """
        _user_1 = User.objects.create_user(
            email="exist@test.local",
            username="exist_local",
            password="T@eST1926",
        )
        _user_2 = User.objects.create_user(
            email="exist_other@test.local",
            username="exist_other_local",
            password="T@eST1926",
        )
        _permission = Permission.objects.filter(
            codename__in=[
                "view_post",
                "add_post",
                "change_post",
                "delete_post",
                "view_comment",
                "add_comment",
                "change_comment",
                "delete_comment",
            ]
        ).values_list("id", flat=True)
        _user_1.user_permissions.add(*_permission)
        _user_2.user_permissions.add(*_permission)
        self.client = APIClient()

    @staticmethod
    def get_token(user):
        """
        get token
        :param user:
        :return:
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def post_create(user):
        """
        post create
        :param user:
        :return:
        """
        _profile, _ = Profile.objects.get_or_create(bio="test", user=user)
        _post = Post.objects.create(title="test", content="test", author=_profile)
        return _post

    @staticmethod
    def perms(comment, user):
        """
        assign permission
        :param comment:
        :param user:
        :return:
        """
        assign_perm("delete_comment", user, comment)

    @staticmethod
    def comment_create(user, post):
        """
        comment create
        :param user:
        :param post:
        :return:
        """
        _profile, _ = Profile.objects.get_or_create(bio="test", user=user)
        _comment = Comment.objects.create(post=post, author=_profile, content="test")
        return _comment

    def test_comment_create(self):
        """
        test create comment
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _post = self.post_create(_user)
        _data = {
            "post": _post.id,
            "content": "test",
        }
        response = self.client.post(
            "/api/comments/", _data, headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 201)

    def test_comment_list(self):
        """
        test list comment
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        response = self.client.get(
            f"/api/comments/", headers={"Authorization": f"Bearer {_token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_delete(self):
        """
        test delete comment
        :return:
        """
        _user = User.objects.get(email="exist@test.local")
        _token = self.get_token(_user)
        _post = self.post_create(_user)
        _comment = self.comment_create(_user, _post)
        self.perms(_comment, _user)
        response = self.client.delete(
            f"/api/comments/{_comment.id}/",
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 204)

    def test_comment_delete_permission_denied(self):
        """
        test delete comment permission denied
        :return:
        """
        _user = User.objects.get(email="exist_other@test.local")
        _token = self.get_token(_user)
        _post = self.post_create(_user)
        _comment = self.comment_create(_user, _post)
        response = self.client.delete(
            f"/api/comments/{_comment.id}/",
            headers={"Authorization": f"Bearer {_token}"},
        )
        self.assertEqual(response.status_code, 403)

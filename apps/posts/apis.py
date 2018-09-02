from tastypie.resources import ModelResource
from apps.posts.models import Post, Like,Comment
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie import fields
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from .authorization import PostAuthorization
from apps.common.valide_user import ValideUserRegister, ValideUserLogin
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden
from .authorization import LikeAuthorization,CommentAuthorization,PostAuthorization
from apps.accounts.apis import UserResource


class PostResource(ModelResource):
    """
        see,update,create post
    """

    author = fields.ForeignKey(UserResource, attribute='author')
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
        allowed_methods = ["get", "put", "delete","post"]
        # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
        authorization = PostAuthorization()
        always_return_data = True
        
    def hydrate(self, bundle):
        # print(bundle.obj.image)
        # print(dir(bundle.obj))

        # print(bundle.request.user)
        # print(bundle.data.values())
        author = bundle.request.user
        # author_data = {"id":bundle.request.user.id,"username":bundle.request.user.username,"profile":None
        #                }
        bundle.data["author"] = author
        return super(PostResource, self).hydrate(bundle)

class CommentResource(ModelResource):
    post = fields.ForeignKey(PostResource, attribute='post')
    commenter = fields.ForeignKey(UserResource, attribute='commenter')
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        allowed_methods = ["get", "put", "delete","post"]
        # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
        authorization = CommentAuthorization()
        always_return_data = True
        
    def obj_create(self, bundle, **kwargs):
        print(bundle.data["post"])
        post = Post.objects.get(id=bundle.data["post"]["id"])
        post.count_comment = post.count_comment+1
        post.save()
        return super(CommentResource, self).obj_create(bundle, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        post = Post.objects.get(bundle.data["id"])
        post.count_comment = post.count_comment-1
        post.save()
        return super(CommentResource, self).obj_create(bundle, **kwargs)


class LikeResource(ModelResource):
    class Meta:
        queryset = Like.objects.all()
        resource_name = 'reaction'
        allowed_methods = ["get", "put", "delete"]
        # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
        authorization = LikeAuthorization()
        always_return_data = True

    def prepend_urls(self):
        from django.conf.urls import url
        from tastypie.utils import trailing_slash
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/like%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('like_post'), name="api_like"),

            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/unlike%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('unlike_post'), name="api_unlike"),
        ]

    def like_post(self, request, **kwargs):
        pk_post = request.resolver_match.kwargs["pk"]
        id_user = request.user.id

        # post = Post.objects.get(author__post__count_like=2)
        like = Like.objects.filter(liker_id=id_user,post_id=pk_post).first()
        print(like)
        if like is None:
            post = Post.objects.get(id=pk_post)
            post.count_like = post.count_like + 1
            post.save()
            Like.objects.create(liker_id=id_user,post_id=pk_post)
            return self.create_response(request, {
                'message': 'like post sucess'
            }, HttpForbidden)
        else:
            raise BadRequest("have liked before")

    def unlike_post(self, request, **kwargs):
        pk_post = request.resolver_match.kwargs["pk"]
        id_user = request.user.id

        # post = Post.objects.get(author__post__count_like=2)
        like = Like.objects.filter(liker_id=id_user, post_id=pk_post).first()
        if like is not None:
            post = Post.objects.get(id=pk_post)
            post.count_like = post.count_like -1
            Like.objects.get(liker_id=id_user, post_id=pk_post).delete()
            post.save()
            return self.create_response(request, {
                'message': 'unlike post sucess'
            }, HttpForbidden)
        else:
            raise BadRequest("you haven't liked before ")

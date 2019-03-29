from apps.products.models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError, models
from tastypie import fields
from tastypie.authentication import (ApiKeyAuthentication, Authentication,
                                     BasicAuthentication, MultiAuthentication)
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie.models import create_api_key
from tastypie.resources import ModelResource


class CategoryResource(ModelResource):
    """
        see,update,create product
    """
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        allowed_methods = ["get", "put", "delete","post"]
        # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
    

class ProductResource(ModelResource):
    """
        see,update,create product
    """
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'products'
        allowed_methods = ["get", "put", "delete","post"]
        # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        
class ProductHotResource(ModelResource):
    """
        see hotproduct
    """
    class Meta:
        queryset = Product.objects.all().order_by('-numberBuy')
        resource_name = 'products_hot'
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

class ProductNewResource(ModelResource):
    """
        see new product
    """
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'products_new'
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
# class CommentResource(ModelResource):
#     post = fields.ForeignKey(PostResource, attribute='post')
#     commenter = fields.ForeignKey(UserResource, attribute='commenter')
#     class Meta:
#         queryset = Comment.objects.all()
#         resource_name = 'comment'
#         allowed_methods = ["get", "put", "delete","post"]
#         # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
#         authentication = ApiKeyAuthentication()
#         authorization = CommentAuthorization()
#         always_return_data = True
        
#     def obj_create(self, bundle, **kwargs):
#         print(bundle.data["post"])
#         post = Post.objects.get(id=bundle.data["post"]["id"])
#         post.count_comment = post.count_comment+1
#         post.save()
#         return super(CommentResource, self).obj_create(bundle, **kwargs)

#     def obj_delete(self, bundle, **kwargs):
#         post = Post.objects.get(bundle.data["id"])
#         post.count_comment = post.count_comment-1
#         post.save()
#         return super(CommentResource, self).obj_create(bundle, **kwargs)


# class LikeResource(ModelResource):
#     class Meta:
#         queryset = Like.objects.all()
#         resource_name = 'reaction'
#         allowed_methods = ["get", "put", "delete"]
#         # fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
#         authentication = ApiKeyAuthentication()
#         authorization = LikeAuthorization()
#         always_return_data = True

#     def prepend_urls(self):
#         from django.conf.urls import url
#         from tastypie.utils import trailing_slash
#         return [
#             url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/like%s$" % (
#                 self._meta.resource_name, trailing_slash()),
#                 self.wrap_view('like_post'), name="api_like"),

#             url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/unlike%s$" % (
#                 self._meta.resource_name, trailing_slash()),
#                 self.wrap_view('unlike_post'), name="api_unlike"),
#         ]

#     def like_post(self, request, **kwargs):
#         pk_post = request.resolver_match.kwargs["pk"]
#         id_user = request.user.id

#         # post = Post.objects.get(author__post__count_like=2)
#         like = Like.objects.filter(liker_id=id_user,post_id=pk_post).first()
#         print(like)
#         if like is None:
#             post = Post.objects.get(id=pk_post)
#             post.count_like = post.count_like + 1
#             post.save()
#             Like.objects.create(liker_id=id_user,post_id=pk_post)
#             return self.create_response(request, {
#                 'message': 'like post sucess'
#             }, HttpForbidden)
#         else:
#             raise BadRequest("have liked before")

#     def unlike_post(self, request, **kwargs):
#         pk_post = request.resolver_match.kwargs["pk"]
#         id_user = request.user.id

#         # post = Post.objects.get(author__post__count_like=2)
#         like = Like.objects.filter(liker_id=id_user, post_id=pk_post).first()
#         if like is not None:
#             post = Post.objects.get(id=pk_post)
#             post.count_like = post.count_like -1
#             Like.objects.get(liker_id=id_user, post_id=pk_post).delete()
#             post.save()
#             return self.create_response(request, {
#                 'message': 'unlike post sucess'
#             }, HttpForbidden)
#         else:
#             raise BadRequest("you haven't liked before ")

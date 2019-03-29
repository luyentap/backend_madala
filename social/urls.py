"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from apps.accounts.apis import (AuthenResource, FriendResource,
                                ProfileResource, UserResource)
from apps.posts.apis import CommentResource, LikeResource, PostResource
from apps.products.apis import (CategoryResource, ProductHotResource,
                                ProductNewResource, ProductResource)
from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(AuthenResource())
v1_api.register(ProfileResource())
v1_api.register(FriendResource())

v1_api.register(CommentResource())
v1_api.register(LikeResource())
v1_api.register(PostResource())

v1_api.register(CategoryResource())
v1_api.register(ProductResource())
v1_api.register(ProductHotResource())
v1_api.register(ProductNewResource())


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^post/', include('apps.posts.urls')),
    url('api/', include(v1_api.urls)),


]

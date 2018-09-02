from tastypie.resources import ModelResource
from apps.accounts.models import Profile, Friend
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
from .authorization import UserAuthorization
from apps.common.valide_user import ValideUserRegister, ValideUserLogin
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden

# import signal: once a while, user register, create api_key
from .singals import *


class ProfileResource(ModelResource):
    """
        see,update profile
    """

    # user = fields.ForeignKey(UserResource, attribute='user', full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods = ["get", "put", "delete"]
        fields = ['id', 'username', 'address', 'birthday', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        always_return_data = True

    # def dehydrate(self, bundle):
    #     bundle.data['user_id'] = bundle.obj.user.id
    #     bundle.data['username'] = bundle.obj.user.username
    #     bundle.data['first_name'] = bundle.obj.user.first_name
    #     bundle.data['last_name'] = bundle.obj.user.last_name
    #     return bundle


class UserResource(ModelResource):
    profile = fields.ForeignKey(ProfileResource, attribute='profile', full=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        # must authorization : create profile(user+ detail)
        authorization = UserAuthorization()
        excludes = ["password"]
        allowed_methods = ["get", "put", "delete"]
        fields = ['id', 'username', 'first_name', 'last_name']
        always_return_data = True

    def hydrate(self, bundle):
        # profile = Profile.objects.get(user=User.objects.get(id=bundle.obj.id))
        profile = Profile.objects.get(id=bundle.obj.profile.pk)
        profile.address = bundle.data["address"]
        profile.birthday = bundle.data["birthday"]
        profile.save()
        return super(UserResource, self).hydrate(bundle)


class AuthenResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "authen"

    def prepend_urls(self):
        from django.conf.urls import url
        from tastypie.utils import trailing_slash
        return [
            url(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),

            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),

            url(r"^(?P<resource_name>%s)/logout%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name="api_logout"),

        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data["username"]
        password = data["password"]
        email = data["email"]

        # validation : username and pass,email: common package
        valid_user = ValideUserRegister()
        if (valid_user.is_username(username=username) & valid_user.is_email(email=email) & valid_user.is_password(
                password=password)):
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            profile = data["profile"]
            address = profile["address"]
            birthday = profile["birthday"]
            profile = Profile(user=user, birthday=birthday, address=address)
            # validation and profile: common package
            # ..
            profile.save()

            print(username, password, email, profile)
            return self.create_response(request, {
                "id": user.id,
                "username": username,
                "email": email,
                "profile": {
                    "id": profile.id,
                    "birthday": birthday,
                    "address": address,
                }
            })
        return self.create_response(request, {"message_error": valid_user.error_message})

    def logout(self, request, **kwargs):
        """
        A new end point to logout the user using the django login system
        """
        self.method_check(request, allowed=['get'])
        print(request.user)
        if request.user and request.user.is_authenticated():
            logout(request)
            print(request.user)

            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False,
                                                  'error_message': 'You are not authenticated, %s' % request.user.is_authenticated()})

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        # validation here before authenticate
        valid = ValideUserLogin()
        if valid.is_exists(username=username):
            user = authenticate(username=username, password=password)
        else:
            raise BadRequest("username isn't exists ")
        if user:
            if user.is_active:
                login(request, user)

                return self.create_response(request, {
                    "apikey ": user.api_key.key,
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,

                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)


class FriendResource(ModelResource):
    class Meta:
        queryset = Friend.objects.all()
        resource_name = 'friend'
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        always_return_data = True

    def prepend_urls(self):
        from django.conf.urls import url
        from tastypie.utils import trailing_slash
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/send_request%s$" % (
            self._meta.resource_name, trailing_slash()),
                self.wrap_view('send_request'), name="api_sending"),

            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/accept_request%s$" % (
            self._meta.resource_name, trailing_slash()),
                self.wrap_view('accept_request'), name="api_accepting"),

            url(r"^(?P<resource_name>%s)/(?P<pk>[\w\d_.-]+)/reset_request%s$" % (
            self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_request'), name="api_resetting"),

        ]

    def send_request(self, request, **kwargs):
        pk_friend = request.resolver_match.kwargs["pk"]
        id_user = request.user.id
        relationship = Friend.objects.filter(friend=User.objects.get(id=pk_friend)).first() or Friend.objects.filter(
            friend=User.objects.get(id=id_user),user=User.objects.get(id=pk_friend)).first()
        # Friend.objects.get()
        print(relationship.is_friend)
        if relationship is None:
            f = Friend.objects.create(user_id=id_user,status=1,friend_id=pk_friend)
            print(f)

            return self.create_response(request, {
                'message' : 'request friend success'
            }, HttpForbidden)

        if relationship.is_friend == 1 :
            raise  BadRequest("is a friend before");
        if relationship.status  == '1':
            raise BadRequest("had a friend  request before");


        raise BadRequest("username isn't exists ")

    def accept_request(self, request, **kwargs):
        pk_friend = request.resolver_match.kwargs["pk"]
        id_user = request.user.id
        relationship = Friend.objects.filter(friend=User.objects.get(id=pk_friend)).first() or Friend.objects.filter(
            friend=User.objects.get(id=id_user), user=User.objects.get(id=pk_friend)).first()
        # Friend.objects.get()
        if relationship is not None:
            if relationship.is_friend == 1:
                raise BadRequest("is a friend before")
            else:
                relationship.status = '2'
                relationship.is_friend = 1
                relationship.save()
                return self.create_response(request, {
                    'message': 'accept friend success'
                }, HttpForbidden)

        raise BadRequest("didn't have a request to accept")


    def reset_request(self, request, **kwargs):
        pk_friend = request.resolver_match.kwargs["pk"]
        id_user = request.user.id
        relationship = Friend.objects.filter(friend=User.objects.get(id=pk_friend)).first() or Friend.objects.filter(
            friend=User.objects.get(id=id_user), user=User.objects.get(id=pk_friend)).first()
        # Friend.objects.get()
        if relationship is not None:
            if relationship.is_friend == 1 or relationship.status == '1':
                relationship.status = '0'
                relationship.is_friend = 0
                relationship.save()
                return self.create_response(request, {
                    'message': 'reset relationship success'
                }, HttpForbidden)

        raise BadRequest("didn't have a relationshio to reset")

from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class PostAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        print(bundle.obj)
        print(bundle.obj.author)

        return bundle.obj.author == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.author == bundle.request.user

class CommentAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.commenter == bundle.request.user


class LikeAuthorization(Authorization):
    def delete_detail(self, object_list, bundle):
        return bundle.obj.liker == bundle.request.user

    def create_detail(self, object_list, bundle):
        return bundle.obj.liker == bundle.request.user

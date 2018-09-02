from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        print(bundle.obj)
        print(bundle.request.user)
        return bundle.obj == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

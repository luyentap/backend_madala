from django.contrib import admin
from apps.accounts.models import Profile,Friend

# Register your models here.
admin.register(Profile)(admin.ModelAdmin)
admin.register(Friend)(admin.ModelAdmin)
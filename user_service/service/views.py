# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views import View
from django.core import serializers

from .models import User


# @require_POST()
class NewUserView(View):
    pass


class UserView(View):
    def get(self, request, username, *args, **kwargs):
        try:
            user_info = User.objects.get(login=username).values('login', 'name')
        except User.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        data = serializers.serialize('json', user_info)
        return HttpResponse(data, content_type='application/json')

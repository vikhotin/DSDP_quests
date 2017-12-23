from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import User
from .forms import UserForm


class NewUserView(View):
    http_method_names = ['post']

    # this method turns off csrf check
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NewUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/{}/'.format(form.cleaned_data['login']))


class UserView(View):
    def get(self, request, username, *args, **kwargs):
        try:
            User.objects.defer('password')
            user_info = User.objects.get(login=username)
        except User.DoesNotExist:
            return HttpResponse('[]', content_type='application/json', status=404)
        user_json = user_info.to_json()
        return JsonResponse(user_json, safe=False)

# Django
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import (
    FormView
)
from django.views.generic import (View)

# Apps
from apps.locals.models import Local
from .forms import (
    LoginForm,
)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.type_user == '1':
            ls = Local.objects.filter(owner=self.request.user)
        elif self.request.user.type_user == '2':
            ls = Local.objects.filter(manager__manager=self.request.user)
        return reverse_lazy('locals_app:panel', kwargs={'local': ls.first().slug})

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

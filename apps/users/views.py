# Django
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import (
    FormView
)
from django.views.generic import (View)

# Apps
from .forms import (
    LoginForm,
)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('locals_app:panel')

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

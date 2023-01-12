# Django
# from ast import Try
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import (
    FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.views.generic import (View)

# Apps
# from apps.users.models import User
from apps.locals.models import Local
from .forms import (
    LoginForm,
)
import datetime


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('sales_app:panel_su')
        else:
            # if self.request.user.type_user == '1':
            #     ls = Local.objects.filter(owner=self.request.user)
            # elif self.request.user.type_user == '2':
            #     ls = Local.objects.filter(manager__manager=self.request.user)
            return reverse_lazy('users_app:panel')

    def form_valid(self, form):
        user = authenticate(
            dni=form.cleaned_data['dni'],
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


class PanelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if self.request.user.type_user == '1':
            ls = Local.objects.filter(owner=request.user)
        elif request.user.type_user == '2':
            ls = Local.objects.filter(manager__manager=request.user)

        return render(request, 'users/panel.html', {
            'locals': ls,
            'today': datetime.datetime.today()
        })

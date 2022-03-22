from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View, )
from django.shortcuts import render, redirect
from django.contrib import messages
# from datetime import timedelta

# apps
from apps.locals.models import Local
from apps.locals.forms import ManagerForm, UserUpdateForm
from apps.users.models import User
from apps.locals.models import Manager, Employee

# other
from dateutil.relativedelta import relativedelta
import datetime
# from datetime import date


class PanelView(LoginRequiredMixin, View):
    def get(self, request, local, *args, **kwargs):
        if self.request.user.type_user == '1':
            ls = Local.objects.filter(owner=self.request.user)
        elif self.request.user.type_user == '2':
            ls = Local.objects.filter(manager__manager=self.request.user)

        return render(request, 'locals/list.html', {
            'locals': ls,
            'local': Local.objects.get(slug=local),
        })


class ManagerCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm(),
            'local': local
        })

    def post(self, request, local, *args, **kwargs):
        form = ManagerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(local=local, type_user='manager')
            messages.add_message(request, messages.SUCCESS, 'Gerente creado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form
        })


class ManagerUpdateView(View):

    def get(self, request, local, pk, *args, **kwargs):
        return render(request, 'locals/manager/update_manager.html', {
            'form': UserUpdateForm(instance=User.objects.get(pk=pk)),
            'local': local,
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Gerente editado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': local
        })


class ManagerDeleteView(LoginRequiredMixin, View):
    def post(self, request, local, pk, *args, **kwargs):
        # Manager.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Gerente Eliminado')
        return redirect('locals_app:panel', local=local)


# Employe
class EmployeeCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm(),
            'local': local
        })

    def post(self, request, local, *args, **kwargs):
        form = ManagerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(local=local, type_user='employee')
            messages.add_message(request, messages.SUCCESS, 'Empleado creado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': local
        })


class EmployeeUpdateView(View):

    def get(self, request, local, pk, *args, **kwargs):
        return render(request, 'locals/manager/update_manager.html', {
            'form': UserUpdateForm(instance=User.objects.get(pk=pk)),
            'local': local
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Empleado editado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': local
        })


class EmployeeDeleteView(LoginRequiredMixin, View):
    def post(self, request, local, pk, *args, **kwargs):
        Employee.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Empleado Eliminado')
        return redirect('locals_app:panel', local=local)


class RenovateView(LoginRequiredMixin, View):
    def get(self, request, pk, days, *args, **kwargs):
        # e = Employee.objects.filter(pk=pk)
        # timedelta(days)
        # td = e[0].due_date + relativedelta(months=1)
        print(datetime.datetime(2024, 10, 21) + relativedelta(day=31))

        # e.update(due_date=td)
        messages.add_message(request, messages.SUCCESS, 'Empleado Renovado')

        return redirect('locals_app:panel')


def generate_qrcode(request):
    return render(request, 'qr.html')


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

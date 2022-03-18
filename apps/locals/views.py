from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View, ListView)
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, timedelta

# apps
from apps.locals.models import Local
from apps.locals.forms import ManagerForm, UserUpdateForm
from apps.users.models import User
from apps.locals.models import Manager, Employee


class PanelView(LoginRequiredMixin, ListView):
    template_name = "locals/list.html"
    context_object_name = 'locals'

    def get_queryset(self):
        if self.request.user.type_user == '1':
            return Local.objects.filter(owner=self.request.user)
        elif self.request.user.type_user == '2':
            return Local.objects.filter(manager__manager=self.request.user)


class ManagerCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm()
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
            'form': UserUpdateForm(instance=User.objects.get(pk=pk))
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Gerente editado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form
        })


class ManagerDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        Manager.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Gerente Eliminado')
        return redirect('locals_app:panel')


# Employe
class EmployeeCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm()
        })

    def post(self, request, local, *args, **kwargs):
        form = ManagerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(local=local, type_user='employee')
            messages.add_message(request, messages.SUCCESS, 'Empleado creado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form
        })


class EmployeeUpdateView(View):

    def get(self, request, local, pk, *args, **kwargs):
        return render(request, 'locals/manager/update_manager.html', {
            'form': UserUpdateForm(instance=User.objects.get(pk=pk))
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Empleado editado')
            return redirect('locals_app:panel')
        return render(request, 'locals/manager/add_manager.html', {
            'form': form
        })


class EmployeeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        Employee.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Empleado Eliminado')
        return redirect('locals_app:panel')


class RenovateView(LoginRequiredMixin, View):
    def get(self, request, pk, days, *args, **kwargs):
        e = Employee.objects.filter(pk=pk)
        td = e[0].due_date + timedelta(days)
        e.update(due_date=td)
        messages.add_message(request, messages.SUCCESS, 'Empleado Renovado')
        return redirect('locals_app:panel')

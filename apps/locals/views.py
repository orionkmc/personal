from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View, )
from django.shortcuts import render, redirect
from django.contrib import messages

# apps
from apps.locals.models import Local, Manager
from apps.locals.forms import ManagerForm, UserUpdateForm
from apps.users.models import User
from apps.locals.models import Employee

# other
from dateutil.relativedelta import relativedelta
import datetime
# from datetime import date


def local_(user):
    if user.type_user == '1':
        return Local.objects.filter(owner=user)
    elif user.type_user == '2':
        return Local.objects.filter(manager__manager=user)


class UserView(View):
    def get(self, request, dni, *args, **kwargs):
        context = {}
        try:
            user = User.objects.get(dni=dni)

            a = datetime.date.today()
            # a = datetime.datetime(2022, 4, 1)
            for x in user.employee.all():
                if x.due_date.strftime("%Y-%m-%d") >= a.strftime("%Y-%m-%d"):
                    context['valid'] = True

            context['user'] = user
            context['exist'] = True
        except Exception as e:
            print(e)
            context['exist'] = False

        return render(request, 'user.html', context)


class PanelView(LoginRequiredMixin, View):
    def get(self, request, local, *args, **kwargs):
        a = datetime.date.today() + relativedelta(day=31)
        b = datetime.date.today()
        # a = datetime.datetime(2022, 3, 29) + relativedelta(day=31)
        # b = datetime.datetime(2022, 3, 29)
        c = a - b
        if c.days < 3:
            renovate = True
        else:
            renovate = False

        return render(request, 'locals/list.html', {
            'locals': local_(self.request.user),
            'local': Local.objects.get(slug=local),
            'renovate': renovate,
        })


class ManagerCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm(),
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })

    def post(self, request, local, *args, **kwargs):
        form = ManagerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(local=local, type_user='manager')
            messages.add_message(request, messages.SUCCESS, 'Gerente creado')
            return redirect('locals_app:panel', local=local)
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })


class ManagerUpdateView(View):
    def get(self, request, local, pk, *args, **kwargs):
        return render(request, 'locals/manager/update_manager.html', {
            'form': UserUpdateForm(instance=User.objects.get(pk=pk)),
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Gerente editado')
            return redirect('locals_app:panel', local=local)
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })


class ManagerDeleteView(LoginRequiredMixin, View):
    def post(self, request, local, pk, *args, **kwargs):
        Manager.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Gerente Eliminado')
        return redirect('locals_app:panel', local=local)


# Employe
class EmployeeCreateView(View):
    def get(self, request, local, *args, **kwargs):
        return render(request, 'locals/manager/add_manager.html', {
            'form': ManagerForm(),
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })

    def post(self, request, local, *args, **kwargs):
        form = ManagerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(local=local, type_user='employee')
            messages.add_message(request, messages.SUCCESS, 'Empleado creado')
            return redirect('locals_app:panel', local=local)
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })


class EmployeeUpdateView(View):

    def get(self, request, local, pk, *args, **kwargs):
        return render(request, 'locals/manager/update_manager.html', {
            'form': UserUpdateForm(instance=User.objects.get(pk=pk)),
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })

    def post(self, request, local, pk, *args, **kwargs):
        form = UserUpdateForm(request.POST, request.FILES, instance=User.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Empleado editado')
            return redirect('locals_app:panel', local=local)
        return render(request, 'locals/manager/add_manager.html', {
            'form': form,
            'local': Local.objects.get(slug=local),
            'locals': local_(request.user),
        })


class EmployeeDeleteView(LoginRequiredMixin, View):
    def post(self, request, local, pk, *args, **kwargs):
        Employee.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Empleado Eliminado')
        return redirect('locals_app:panel', local=local)


class RenovateView(LoginRequiredMixin, View):
    def get(self, request, local, pk, days, *args, **kwargs):
        e = Employee.objects.filter(pk=pk)
        # td = e[0].due_date + relativedelta(months=1)

        td = datetime.date.today() + relativedelta(months=1)
        # td = datetime.datetime(2022, 3, 28) + relativedelta(months=1)
        e.update(due_date=td)

        messages.add_message(request, messages.SUCCESS, 'Empleado Renovado')
        return redirect('locals_app:panel', local=local)

from django.shortcuts import render
from django.views.generic import (View, )


# views
class SalesView(View):
    def get(self, request, *args, **kargs):
        context = {}
        return render(request, 'sales/index.html', context)

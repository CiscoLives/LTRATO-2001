from django.shortcuts import render
from django.http import HttpResponse

from .device import get_interfaces

# Create your views here.


def index(request):
    interface_list = get_interfaces()
    return HttpResponse(str(interface_list))

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from typing import Union

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
  return redirect('post_list')




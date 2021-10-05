from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "main page/index.htm")
def test(request):
    return render(request, "main page/test.htm")

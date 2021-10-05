from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "frontend/main_page.htm")
def test(request):
    return render(request, "frontend/test.htm")

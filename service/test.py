from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

def test(request):
    return render(request, "test.html", {})
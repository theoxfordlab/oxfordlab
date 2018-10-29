from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


# Create your views here.


def home(req):
    return render(request=req, template_name="index.html")


def login_user(request):
    print("Here")
    logout(request)
    user_name = password = ''
    if request.POST:
        print("Here1")
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=user_name, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render(request, 'login.html')


@login_required(login_url='/main/')
def main(request):
    print("My name is abrar khan")
    return render(request=request, template_name="index.html")

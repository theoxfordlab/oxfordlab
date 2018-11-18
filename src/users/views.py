from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import SignUpForm


def home(req):
    return render(request=req, template_name="index.html")


def login_user(request):
    logout(request)
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET.get("next"):
                    return HttpResponseRedirect(request.GET["next"])
                return HttpResponseRedirect("/manage_urls/")
    return render(request, "login.html")


# @login_required(login_url='/main/')
def main(request):
    return render(request=request, template_name="base.html")


def registration(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        for field in user_form:
            for error in field.errors:
                print("Error ", error)
        if user_form.is_valid():
            user = user_form.save()
            # f_name = user_form.cleaned_data['first_name']
            # l_name = user_form.cleaned_data['last_name']
            # username = f_name + l_name
            # raw_password = user_form.cleaned_data['password1']
            # user = authenticate(username=username, password=raw_password)
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return redirect("/")
        else:
            return render(request, "signup.html", {"form": user_form})

    form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request=request, template_name="index.html")

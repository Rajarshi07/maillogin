from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,WhitelistDomain,BlacklistDomain
from .utils import EmailCheck
from django.contrib.auth.decorators import login_required

# Create your views here.
def loggin(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect(home)
        else:
            return render(
                request,
                "users/login.html",
                {"error": "Email or password is incorrect"},
            )
    return render(request, "users/login.html", {"error": ""})


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:
            createacc,activateacc,message = EmailCheck(email)
            if(not createacc):
                return render(
                    request,
                    "users/register.html",
                    {"error": message},
                )
            try:
                user = CustomUser.objects.create_user(email, password,)
                user.save()
                return render(
                    request,
                    "users/register.html",
                    {"error": message},
                )
            except:
                return render(
                    request,
                    "users/register.html",
                    {"error": "Email already exists"},
                )
        else:
            return render(
                request,
                "users/register.html",
                {"error": "Password and Confirm Password does not match"},
            )
    return render(request, "users/register.html")

def home(request):
    return render(request,"home.html")
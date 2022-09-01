from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,WhitelistDomain,BlacklistDomain
from .utils import EmailCheck
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
User = get_user_model()

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
            print(createacc,activateacc,message)
            if(not createacc):
                return render(
                    request,
                    "users/register.html",
                    {"error": message},
                )
            try:
                user = CustomUser.objects.create_user(email, password,is_active=False)
                user.save()
            except Exception as e:
                print(e)
                return render(
                    request,
                    "users/register.html",
                    {"error": "Email already exists"},
                )
            try:
                current_site = get_current_site(request)
                mail_subject = 'Activate your maillogin account.'
                mail_message = render_to_string('activation_mail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail = EmailMessage(
                    mail_subject, mail_message, to=[email]
                )
                mail.send()
                return render(
                    request,
                    "users/register.html",
                    {"error": message},
                )
            except Exception as e:
                print(e)
                return render(
                    request,
                    "users/register.html",
                    {"error": "Error sending activation mail. Contact audit team to activate account."},
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


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
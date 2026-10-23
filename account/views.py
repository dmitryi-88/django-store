from django.shortcuts import redirect, render
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("register")

    else:
        form = RegistrationForm()

    templ = "account/register.html"
    data = {"form": form}

    return render(request, templ, data)

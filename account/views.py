from .forms import RegisterUserForm
from django.shortcuts import redirect, render


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = RegisterUserForm()
        context = {
            'form' : form
        }
        return render(request, 'registration/register.html', context)



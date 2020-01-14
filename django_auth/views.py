from django.shortcuts import redirect, reverse, render
from django.contrib import auth, messages
from .forms import UserLoginForm


def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect(reverse('login'))


def login(request):
    """Provide a login page"""
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['email'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You have been logged in')
                if user.is_admin:
                    return redirect('/admin/')
                return redirect('/profile/')
            
            else:
                login_form.add_error(None,
                "Your email address or password in incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView

from Student.models import Student
from Employer.models import Employer
from Admin.models import Admin

def isValidated(passwd):
    special_symbols = {'$', '@', '%', '&', '?', '.', '!', '#', '*', ' '}
    status = True

    if len(passwd) > 8:
        status = True

    if not any(char.isdigit() for char in passwd): 
        status = False
          
    if not any(char.isupper() for char in passwd): 
        status = False
          
    if not any(char.islower() for char in passwd): 
        status = False
          
    if not any(char in special_symbols for char in passwd): 
        status = False
        
    return status

def login(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is None:
                messages.info(request, 'Credentials do not exist, please try a different username/password')
                return redirect("log_in")
            else:
                auth.login(request, user)
                print('User logged in')
                return render(request, "index.html", get_user_type(request))
    else:
        return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        return redirect("/")
    else:
        return render(request, 'forgot_password.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

# def confirm_logout(request):
#     return render(request, 'logout.html')

# def cancel_logout(request):
#     return redirect("/")

def get_user_type(request):
    type = 'none'
    args = {'user_type': type}

    try:
        e = Employer.objects.get(user_id=request.user.id)
        type = 'employer'
        args = {'user_type': type, 'obj': e}
    except Employer.DoesNotExist:
        pass

    try:
        s = Student.objects.get(user_id=request.user.id)
        type = 'student'
        args = {'user_type': type, 'obj': s}
    except Student.DoesNotExist:
        pass

    try:
        a = Admin.objects.get(user_id=request.user.id)
        type = 'admin'
        args = {'user_type': type, 'obj': a}
    except Admin.DoesNotExist:
        pass

    return args
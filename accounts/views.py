from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Get the username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Login the user after successful authentication
                login(request, user)

                # Add success message after successful login
                messages.success(request, "Sign Up successful!")

                # Redirect to home after successful login
                return redirect('welcome')
            else:
                # If authentication fails, add an error message
                messages.error(request, "There was an issue with your registration. Please try again.")
        else:
            # If form is not valid, add an error message
            messages.error(request, "There was an issue with your registration. Please enter the details again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect admin users to the admin panel
                if user.is_superuser:
                    return redirect('/admin/')  # Redirect to Django admin panel
                return redirect('welcome')  # Redirect to home after successful login
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})




# Ensure the user is logged in before accessing this view

def home(request):
    return render(request, 'accounts/home.html')
@login_required
def welcome(request):
    return render(request, 'accounts/welcome.html')  # Default redirect if user type not matched

# Views for each user type's dashboard
@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

@login_required
def mentor_dashboard(request):
    return render(request, 'accounts/mentor_dashboard.html')

@login_required
def instructor_dashboard(request):
    return render(request, 'accounts/instructor_dashboard.html')

@login_required
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page (or any other page)

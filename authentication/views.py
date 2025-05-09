# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile # UserProfile might be created via signal

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Or wherever authenticated users should go

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is created via signal from models.py
            # You can assign a default role if UserProfile has a role field
            # e.g., user.userprofile.role = 'beneficiary'
            # user.userprofile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # This should ideally be handled by the post_save signal in models.py
        user_profile = UserProfile.objects.create(user=request.user)

    context = {
        'user_profile': user_profile,
        'title': 'User Profile'
    }
    return render(request, 'authentication/profile.html', context)

@login_required
def edit_profile_view(request):
    try:
        user_profile_instance = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile_instance = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile_instance) # request.FILES for image uploads if any
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile_instance)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit Profile'
    }
    return render(request, 'authentication/edit_profile.html', context)


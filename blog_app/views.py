from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegistrationForm, UserUpdateForm
from .models import Profile

# ---- Registration View ----
def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      #Add a success message to display on the next page
      messages.success(request, f'Account created for {username}!')
      return redirect('login') # Redirect to the login page
  else:
    form = UserRegistrationForm()
  
  return render(request, 'blog/register.html', {'form': form})

# --- Profile Management View (Basic Implementation)
@login_required
def profile(request):
  # Get or create the user's profile
  
  profile, created = Profile.objects.get_or_create(user=request.user)
  
  if request.method == 'POST':
    # Pass the POST data AND the current instance of the user (request.user)
    user_form = UserUpdateForm(request.POST, instance=request.user)

    if user_form.is_valid():
      user_form.save()

      #User Django's messages framework to provide success feedback
      messages.success(request, f'Your account has been updated!')
      
      return redirect('profile') #Post/Redirect/Get pattern
  else:
    # For a GET request, initialize the form with the current user data
    user_form = UserUpdateForm(instance=request.user)

  context = {
    'user': request.user,
    'profile': profile,
    'title': 'Profile',
    'user_form': user_form
  }

  # Pass the form object to the template
  return render(request, 'blog/profile.html', context)

# --- Profile Edit View
@login_required
def profile_edit(request):
    # Get or create the user's profile
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'title': 'Edit Profile',
        'user_form': user_form
    }
    
    return render(request, 'blog/profile.html', context)

# --- Custom Logout View for debugging
def custom_logout(request):
    print(f"DEBUG: Custom logout called by user: {request.user}")
    logout(request)
    print(f"DEBUG: User logged out, redirecting to login")
    return redirect('login')



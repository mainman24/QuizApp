from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from quizapps.forms import *
# Create your views here.


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
        u_form = UserProfileForm()
    else:
        form = UserCreationForm(data=request.POST)
        u_form = UserProfileForm(data=request.POST)
        if form.is_valid() and u_form.is_valid():
            new_user = form.save(commit=False)
            user_profile = u_form.save(commit=False)
            # form.save()
            print(u_form)
            print()
            print(new_user)
            user_profile.owner = new_user  # save the non commit instance not the form
            #new_user = form.save()
            new_user.save()  # save the non commit instance not the form
            user_profile.save()
            login(request, new_user)
            return redirect('quizapps:index')
    context = {'form': form, 'u_form': u_form}
    return render(request, 'registration/register.html', context)

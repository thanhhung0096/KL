import errno
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Getting static folder path from project settings
            media_dir = settings.MEDIA_ROOT

            # Creating a folder in static directory
            new_dir_path = os.path.join(media_dir, "data/" + user.get_username())
            try:
                os.mkdir(new_dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    # directory already exists
                    pass
                else:
                    print(e)
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

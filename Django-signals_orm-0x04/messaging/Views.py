
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect


@login_required
def delete_user(request):
    user = request.user

    # Log out the user before deleting the account
    logout(request)

    # Delete the user (triggers post_delete signal)
    user.delete()

    return redirect("home")   # redirect to homepage or login page

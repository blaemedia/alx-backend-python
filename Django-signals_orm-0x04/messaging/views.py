from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required
def delete_user(request):
    """
    Allows a logged-in user to permanently delete their account.
    Triggers post_delete signals for cleanup.
    """
    user = request.user

    # Log out before deleting the account
    logout(request)

    # Delete the user account
    user.delete()

    # Redirect after deletion
    return redirect("home")  # Change "home" to your landing page name

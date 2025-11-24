from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from .models import Message


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
    return redirect("home")  # Change "home" if needed


def build_thread(message):
    """
    Recursively gather a message and all nested replies.
    """
    return {
        "id": message.id,
        "sender": message.sender.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [
            build_thread(reply)
            for reply in message.replies.all().order_by("timestamp")
        ]
    }


@login_required
def message_thread(request, message_id):
    """
    Displays a message and all replies in a threaded conversation.
    """
    message = (
        Message.objects
        .select_related("sender", "receiver", "parent_message")
        .prefetch_related("replies__sender", "replies__receiver")
        .get(id=message_id)
    )

    thread = build_thread(message)

    return render(request, "messaging/thread.html", {"thread": thread})

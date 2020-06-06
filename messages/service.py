from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from messages.models import Thread, ChatMessage

def get_user_from_token(auth_token):
    """
    Returns user from auth token
    param : token
    returns : auth_user instance
    """
    return Token.objects.get(key=auth_token).user

def get_user_from_id(user_id):
    """
    Returns user from auth token
    param : auth_user id
    returns : auth_user instance
    """
    return User.objects.get(id=user_id)

def get_thread(user1, user2):
    """
    Gets or creates chat thread between two users.
    param1 : auth_user instance
    param2 : auth_user instance
    """
    q1 = Q(first=user1) & Q(second=user2)
    q2 = Q(first=user2) & Q(second=user1)
    qs = Thread.objects.filter(q1 | q2)
    if qs.count() == 1:
        return qs.first()
    elif qs.count() > 1:
        return qa[0]
    else:
        return Thread.objects.create(first=user1, second=user2)

def save_message(sender, receiver, message):
    """
    Stores the message into the database
    param1 : auth_user instance (sender of message)
    param2 : auth_user instance (receiver of message)
    param3 : auth_user instance (message)
    """
    thread = get_thread(sender, receiver)
    ChatMessage.objects.create(
        thread = thread,
        user = sender,
        message = message
    )
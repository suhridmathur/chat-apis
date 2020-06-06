from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from apis_v1.serializers import UserSerializer, MessageSerializer
from messages.models import ChatMessage
from messages.service import get_thread, get_user_from_id

class Users(APIView):
    def get(self, request, *args, **kwargs):
        """
        API endpoint : /api/v1/users/
        Response Format :
        {
            "status":"Success",
            "payload":[
                {
                    "id" : 1,
                    "first_name" : Suhrid,
                    "last_name" : Mathur,
                    "email" : suhrid@gmail.com,
                }
            ]
        }
        """
        users = User.objects.all().exclude(
            id = request.user.id
        )
        serializer = UserSerializer(users, many=True)
        return Response({
            "status":"Success",
            "payload":serializer.data
        })


class Messages(APIView):
    def get(self, request, *args, **kwargs):
        first = request.user
        second = get_user_from_id(kwargs.get('user_id'))
        thread = get_thread(first, second)
        messages = ChatMessage.objects.filter(
            thread = thread
        )
        serializer = MessageSerializer(messages, many=True)
        return Response({
            "status":"Success",
            "payload":  {
                "my_username" : request.user.username,
                "messages" : serializer.data,
            }
        })
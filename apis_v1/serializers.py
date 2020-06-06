from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, RelatedField, CharField

from messages.models import ChatMessage

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class MessageSerializer(ModelSerializer):
    username = CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['username', 'message']
from rest_framework import serializers
from .models import page

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
"id",
"title",
"body",
)

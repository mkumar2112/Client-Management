from rest_framework import serializers
from .models import *
from django.utils import timezone

class ClientInfoserializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = '__all__'
        # read_only_fields = ['createAt', 'updateAt']

    # def update(self, instance, validated_data):     
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.updateAt = timezone.now().strftime('%Y-%m-%d')  # Automatically set to current date
    #     instance.save()  
    #     print("Note updated successfully")  # Debugging: Confirm the update happened
    #     return instance



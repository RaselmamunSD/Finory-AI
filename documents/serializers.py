"""
Documents module serializers
"""
from rest_framework import serializers
from .models import Document, VoiceCommand


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class VoiceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceCommand
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

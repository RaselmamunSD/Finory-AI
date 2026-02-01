"""
Identity module serializers
"""
from rest_framework import serializers
from .models import Identity, FaceVerification


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FaceVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceVerification
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

"""
AI Engine module serializers
"""
from rest_framework import serializers
from .models import AIModel, AIPrediction, AIRecommendation


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrediction
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

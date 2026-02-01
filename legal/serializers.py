"""
Legal module serializers
"""
from rest_framework import serializers
from .models import Incident, LegalReport, Blacklist


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LegalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

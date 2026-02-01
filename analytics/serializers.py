"""
Analytics module serializers
"""
from rest_framework import serializers
from .models import Dashboard, KPI


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

"""
AI Engine module views
"""
from rest_framework import viewsets, permissions
from .models import AIModel, AIPrediction, AIRecommendation
from .serializers import AIModelSerializer, AIPredictionSerializer, AIRecommendationSerializer


class AIModelViewSet(viewsets.ModelViewSet):
    serializer_class = AIModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AIModel.objects.all()


class AIPredictionViewSet(viewsets.ModelViewSet):
    serializer_class = AIPredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return AIPrediction.objects.filter(company=self.request.tenant)
        return AIPrediction.objects.none()


class AIRecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = AIRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return AIRecommendation.objects.filter(company=self.request.tenant)
        return AIRecommendation.objects.none()

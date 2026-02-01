"""
Core module views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company, Branch, User, Role, CompanyUser
from .serializers import (
    CompanySerializer, BranchSerializer, UserSerializer,
    RoleSerializer, CompanyUserSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company ViewSet
    """
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter by user's companies
        user = self.request.user
        company_ids = CompanyUser.objects.filter(user=user, is_active=True).values_list('company_id', flat=True)
        return Company.objects.filter(id__in=company_ids)
    
    def perform_create(self, serializer):
        company = serializer.save(legal_representative=self.request.user)
        # Create CompanyUser relationship
        owner_role, _ = Role.objects.get_or_create(name='Company Owner', defaults={'is_system_role': True})
        CompanyUser.objects.create(
            company=company,
            user=self.request.user,
            role=owner_role,
            is_active=True
        )


class BranchViewSet(viewsets.ModelViewSet):
    """
    Branch ViewSet
    """
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter by user's companies
        user = self.request.user
        company_ids = CompanyUser.objects.filter(user=user, is_active=True).values_list('company_id', flat=True)
        return Branch.objects.filter(company_id__in=company_ids)


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter by user's companies
        user = self.request.user
        company_ids = CompanyUser.objects.filter(user=user, is_active=True).values_list('company_id', flat=True)
        user_ids = CompanyUser.objects.filter(company_id__in=company_ids).values_list('user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Get or update current user profile
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            })
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    """
    Role ViewSet
    """
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Role.objects.all()


class CompanyUserViewSet(viewsets.ModelViewSet):
    """
    CompanyUser ViewSet
    """
    serializer_class = CompanyUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter by user's companies
        user = self.request.user
        company_ids = CompanyUser.objects.filter(user=user, is_active=True).values_list('company_id', flat=True)
        return CompanyUser.objects.filter(company_id__in=company_ids)

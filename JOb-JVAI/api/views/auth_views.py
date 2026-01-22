"""
Authentication views
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from core.models import User, Company, CompanyUser, Role
import pyotp
import qrcode
from io import BytesIO
import base64


class LoginView(TokenObtainPairView):
    """
    Custom login view with 2FA support
    """
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        two_factor_code = request.data.get('two_factor_code')
        
        if not email or not password:
            return Response({
                'success': False,
                'error': {'message': 'Email and password are required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return Response({
                'success': False,
                'error': {'message': 'Invalid credentials'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'success': False,
                'error': {'message': 'User account is inactive'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check 2FA if enabled
        if user.is_2fa_enabled:
            if not two_factor_code:
                return Response({
                    'success': False,
                    'error': {'message': '2FA code required', 'requires_2fa': True}
                }, status=status.HTTP_200_OK)
            
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(two_factor_code):
                return Response({
                    'success': False,
                    'error': {'message': 'Invalid 2FA code'}
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Get user's companies
        company_users = CompanyUser.objects.filter(user=user, is_active=True)
        companies = [cu.company for cu in company_users]
        
        return Response({
            'success': True,
            'data': {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'is_2fa_enabled': user.is_2fa_enabled,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'companies': [
                    {
                        'id': str(c.id),
                        'name': c.name,
                    } for c in companies
                ]
            }
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
    User registration view
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        company_name = request.data.get('company_name')
        
        if not email or not password:
            return Response({
                'success': False,
                'error': {'message': 'Email and password are required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'error': {'message': 'User with this email already exists'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = User.objects.create_user(email=email, password=password)
        
        # Create company if provided
        company = None
        if company_name:
            company = Company.objects.create(
                name=company_name,
                legal_representative=user
            )
            
            # Get or create default role
            owner_role, _ = Role.objects.get_or_create(
                name='Company Owner',
                defaults={'is_system_role': True}
            )
            
            # Link user to company
            CompanyUser.objects.create(
                company=company,
                user=user,
                role=owner_role,
                is_active=True
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'data': {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'company': {
                    'id': str(company.id),
                    'name': company.name,
                } if company else None
            }
        }, status=status.HTTP_201_CREATED)


class Verify2FAView(generics.GenericAPIView):
    """
    Verify 2FA code view
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        
        if not code:
            return Response({
                'success': False,
                'error': {'message': '2FA code is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_2fa_enabled or not request.user.two_factor_secret:
            return Response({
                'success': False,
                'error': {'message': '2FA is not enabled for this user'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        totp = pyotp.TOTP(request.user.two_factor_secret)
        
        if totp.verify(code):
            return Response({
                'success': True,
                'data': {'message': '2FA code verified'}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': {'message': 'Invalid 2FA code'}
            }, status=status.HTTP_401_UNAUTHORIZED)

"""
Authentication views
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from core.models import User, Company, CompanyUser, Role
from django.utils import timezone
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
        
        # Check if email is verified
        if not user.is_email_verified:
            # Generate new OTP if old one expired
            otp = user.otp_code
            if not otp or (user.otp_expiry and user.otp_expiry < timezone.now()):
                otp = user.generate_otp()
                
            return Response({
                'success': False,
                'error': {
                    'message': 'Email not verified',
                    'requires_verification': True,
                    'otp_debug': otp
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        
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
        full_name = request.data.get('full_name')
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
        user = User.objects.create_user(email=email, password=password, full_name=full_name)
        
        # Generate OTP for email verification
        otp = user.generate_otp()
        
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
            'message': 'Registration Successful',
            'data': {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'full_name': user.full_name,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'company': {
                    'id': str(company.id),
                    'name': company.name,
                } if company else None,
                'otp_debug': otp
            }
        }, status=status.HTTP_201_CREATED)


class VerifyEmailOTPView(generics.GenericAPIView):
    """
    Verify email OTP view
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        user = request.user
        
        if not otp_code:
            return Response({
                'success': False,
                'error': {'message': 'OTP code is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if user.otp_code == otp_code and user.otp_expiry and user.otp_expiry > timezone.now():
            user.is_email_verified = True
            user.otp_code = None
            user.otp_expiry = None
            user.save()
            return Response({
                'success': True,
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': {'message': 'Invalid or expired OTP code'}
            }, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(generics.GenericAPIView):
    """
    Resend OTP view
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        otp = user.generate_otp()
        return Response({
            'success': True,
            'message': 'OTP resent successfully',
            'data': {
                'otp_debug': otp
            }
        }, status=status.HTTP_200_OK)


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


class Setup2FAView(generics.GenericAPIView):
    """
    Setup 2FA view - generates secret and QR code
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_2fa_enabled:
            return Response({
                'success': False,
                'error': {'message': '2FA is already enabled'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        user.save()
        
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(user.email, issuer_name="Finory IA")
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered)
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return Response({
            'success': True,
            'data': {
                'secret': secret,
                'qr_code': f"data:image/png;base64,{qr_code_base64}",
                'provisioning_uri': provisioning_uri
            }
        }, status=status.HTTP_200_OK)


class Enable2FAView(generics.GenericAPIView):
    """
    Enable 2FA view - verifies code and enables 2FA
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get('code')
        
        if not code:
            return Response({
                'success': False,
                'error': {'message': '2FA code is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not user.two_factor_secret:
            return Response({
                'success': False,
                'error': {'message': 'Setup 2FA first'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(code):
            user.is_2fa_enabled = True
            user.save()
            return Response({
                'success': True,
                'message': '2FA enabled successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': {'message': 'Invalid 2FA code'}
            }, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(generics.GenericAPIView):
    """
    Forgot password view - sends OTP to email
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'success': False,
                'error': {'message': 'Email is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            otp = user.generate_password_reset_otp()
            
            return Response({
                'success': True,
                'message': 'Password reset OTP sent successfully',
                'data': {
                    'otp_debug': otp # In production this would be sent via email
                }
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Don't reveal if user exists for security reasons
            return Response({
                'success': True,
                'message': 'If an account exists with this email, a reset OTP has been sent.'
            }, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """
    Reset password view using OTP
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        new_password = request.data.get('new_password')
        
        if not all([email, otp_code, new_password]):
            return Response({
                'success': False,
                'error': {'message': 'Email, OTP code and new password are required'}
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            
            if (user.password_reset_otp == otp_code and 
                user.password_reset_otp_expiry and 
                user.password_reset_otp_expiry > timezone.now()):
                
                user.set_password(new_password)
                user.password_reset_otp = None
                user.password_reset_otp_expiry = None
                user.save()
                
                return Response({
                    'success': True,
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': {'message': 'Invalid or expired OTP code'}
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': {'message': 'Invalid request'}
            }, status=status.HTTP_400_BAD_REQUEST)

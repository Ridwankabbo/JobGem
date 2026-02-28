import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.cache import cache


# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             text_type(user.pk)+text_type(timestamp)+text_type(user.is_active)
#         )
        
# account_activation_token = TokenGenerator()

# ==================== OTP Management ==================
class OtpManagement():
    OTP_EXPIRE_TIME = 300    
    
    def GenerateOTP():
        return str(random.randint(000000, 999999))
    @classmethod
    def store_otp(self, email, otp, purpose):
        key = f"{email}_{purpose}"
        cache.set(key, otp, timeout=self.OTP_EXPIRE_TIME)
        
    @classmethod
    def verifi_otp(self, email, otp, purpose):
        key = f"{email}_{purpose}"
        stored_otp = cache.get(key)
        if stored_otp and stored_otp == otp:
            cache.delete(key)
            
            if purpose == 'password_reset':
                cache.set(f"{email}_password_reset_verified", True, timeout=self.OTP_EXPIRE_TIME)
            return True
        return False
    
    @classmethod
    def is_password_reset_verified(self, email):
        return cache.get(f"{email}_password_reset_verified")
    

def send_otp_mail(email, otp, purpose):
    
    if purpose == 'singup':
        subject = 'verifi you account - OTP'
        message = f"""
Hello,
 
you otp for account verification is : {otp}

This otp will expire in 5 minutes.
If you didn't create an account ignore the email.

Thank you.
"""
    elif purpose == 'password_reset':
        subject = 'reset you password - OTP'
        message = f"""
Hello,
 
you otp for reset password is : {otp}

This otp will expire in 5 minutes.
If you didn't create an account ignore the email.

Thank you.
"""
    else:
        raise ValueError("Invalid otp")
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
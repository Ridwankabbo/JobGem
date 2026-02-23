import random
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)+text_type(timestamp)+text_type(user.is_active)
        )
        
account_activation_token = TokenGenerator()

def GenerateOTP():
    return str(random.randint(000000, 999999))
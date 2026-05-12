import re
from typing import Optional
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from authentication.models import User


class AuthenticationService:
    @classmethod
    def sign_up(cls, data):
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()
        username = data.get("username", "").strip()
        phone_number = data.get("phone_number", "").strip()
        password = data.get("password", "").strip()
        country = data.get("country", "").strip()
        occupation = data.get("occupation", "").strip()

        user = cls.get_user_object(
            email=email,
            # phone_number= phone_number
        )

        if user:
            raise ValidationError(
                "A user with this email or phone number already exists",
                "400"
            )

        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    country=country,
                    occupation=occupation if occupation else None
                )
                return user
            except Exception as e:
                raise ValidationError(
                    f"Failed to create user: {str(e)}",
                    "400"
                )

    @classmethod
    def get_user_object(cls, user_id=None, phone_number=None, email=None):
        if email:
            email = cls.normalize_email(email)
            user = User.objects.filter(email__iexact=email).first()
            if user:
                return user
        if phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                return user
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            if user:
                return user

        return None
        
    @staticmethod
    def normalize_email(email: Optional[str]) -> Optional[str]:
        if not email:
            return None

        return email.strip().lower()

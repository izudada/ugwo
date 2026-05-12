from rest_framework import serializers

from authentication.models import User

class SignUpSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    country = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  "__all__"

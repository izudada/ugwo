from rest_framework import serializers


class GetDebtSerializer(serializers.Serializer):

    country = serializers.CharField()
    year = serializers.DateField(required=False, input_formats=['%Y'])
    start_year = serializers.DateField(required=False, input_formats=['%Y'])
    end_year = serializers.DateField(required=False, input_formats=['%Y'])

# serializers.py
from rest_framework import serializers

class LineDataSerializer(serializers.Serializer):
    line_number = serializers.IntegerField()
    file_name = serializers.CharField(max_length=255)
    random_line = serializers.CharField()
    most_frequent_char = serializers.CharField(max_length=1, allow_null=True)
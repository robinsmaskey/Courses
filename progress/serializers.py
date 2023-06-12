from rest_framework import serializers


class CourseProgressSerializer(serializers.Serializer):
    progress = serializers.IntegerField()

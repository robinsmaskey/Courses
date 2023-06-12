from rest_framework import serializers

from .models import Lesson, Subunit, Unit


class RelatedNameListField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "uid": value.uid,
            "name": value.name,
            "description": value.description,
        }

class SubunitSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    completed = serializers.BooleanField(read_only=True, required=False)
    type = serializers.CharField()

class AuthorizedNestedUnitOutputSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    subunits = SubunitSerializer(many=True, read_only=True, allow_null=True)

class UnauthorizedNestedUnitOutputSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    subunits = SubunitSerializer(source="subunit", many=True, read_only=True, allow_null=True)

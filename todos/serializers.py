# todos/serializers.py
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "user",
            "title",
            "target_date",
            "is_priority",
            "created_on",
            "completed_on",
            "updated_on",
            "status",
        ]
        read_only_fields = ["id", "created_on", "updated_on"]

    def validate_status(self, value):
        valid_statuses = [status[0] for status in Todo.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Choose from {', '.join(valid_statuses)}."
            )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent updating the user
        validated_data.pop("user", None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["status_display"] = instance.get_status_display()
        return representation

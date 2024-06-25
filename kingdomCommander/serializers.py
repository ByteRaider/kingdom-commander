from rest_framework import serializers

class ControlInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    control_type = serializers.CharField()
    automation_id = serializers.CharField()
    class_name = serializers.CharField()
    rect = serializers.JSONField()
    is_enabled = serializers.BooleanField()
    is_visible = serializers.BooleanField()
    parent = serializers.CharField()
    handle = serializers.IntegerField()

class RunningApplicationSerializer(serializers.Serializer):
    title = serializers.CharField()
    class_name = serializers.CharField()
    automation_id = serializers.CharField(allow_null=True)
    process_id = serializers.IntegerField()
    handle = serializers.IntegerField()

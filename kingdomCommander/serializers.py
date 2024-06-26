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

class RectSerializer(serializers.Serializer):
    left = serializers.IntegerField()
    top = serializers.IntegerField()
    right = serializers.IntegerField()
    bottom = serializers.IntegerField()

class ImageSerializer(serializers.Serializer):
    window_text = serializers.CharField()
    automation_id = serializers.CharField()
    handle = serializers.IntegerField()
    rect = RectSerializer()

class StaticTextSerializer(serializers.Serializer):
    window_text = serializers.CharField()
    automation_id = serializers.CharField()
    handle = serializers.IntegerField()
    rect = RectSerializer()

class ComboBoxSerializer(serializers.Serializer):
    window_text = serializers.CharField()
    automation_id = serializers.CharField()
    handle = serializers.IntegerField()
    rect = RectSerializer()

class EditFieldSerializer(serializers.Serializer):
    window_text = serializers.CharField()
    automation_id = serializers.CharField()
    handle = serializers.IntegerField()
    rect = RectSerializer()

class ButtonSerializer(serializers.Serializer):
    window_text = serializers.CharField()
    automation_id = serializers.CharField()
    handle = serializers.IntegerField()
    rect = RectSerializer()

class UIElementsSerializer(serializers.Serializer):
    images = ImageSerializer(many=True)
    static_texts = StaticTextSerializer(many=True)
    comboboxes = ComboBoxSerializer(many=True)
    edit_fields = EditFieldSerializer(many=True)
    buttons = ButtonSerializer(many=True)
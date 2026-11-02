import re

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Skill


ICON_SLUG_PATTERN = re.compile(r"^[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)*$")


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )
    proficiency_display = serializers.CharField(
        source="get_proficiency_display",
        read_only=True,
    )
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    category = serializers.ChoiceField(choices=Skill.CATEGORY_CHOICES)
    proficiency = serializers.ChoiceField(choices=Skill.PROFICIENCY_CHOICES)
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "category",
            "category_display",
            "proficiency",
            "proficiency_display",
            "icon_slug",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Nama skill tidak boleh hanya berisi tag HTML."
            )
        return value

    def validate_icon_slug(self, value):
        value = value.strip()
        if value and not ICON_SLUG_PATTERN.fullmatch(value):
            raise serializers.ValidationError(
                "Slug ikon hanya boleh berisi huruf, angka, '-', '_', dan '/'."
            )
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(
            obj.starred_by.order_by("username").values_list("username", flat=True)
        )
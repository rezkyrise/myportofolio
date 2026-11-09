import re

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Skill


ICON_SLUG_PATTERN = re.compile(r"^[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)*$")

class StarFieldsMixin:
    """Compute star metadata from the prefetched starred_by relation."""

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        usernames = sorted(user.username for user in obj.starred_by.all())
        return ", ".join(usernames)

class SkillSerializer(StarFieldsMixin, serializers.ModelSerializer):
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

class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=Experience.EXPERIENCE_CHOICES,
        required=True,
    )
    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )
    started_at = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"],
    )
    ended_at = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"],
        required=False,
        allow_null=True,
    )
    image = serializers.ImageField(required=False)
    image_url = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "organization",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "image",
            "image_url",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = [
            "id",
            "category_display",
            "image_url",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Judul tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Deskripsi tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value

    def validate_organization(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        start = attrs.get("started_at", getattr(self.instance, "started_at", None))
        end = attrs.get("ended_at", getattr(self.instance, "ended_at", None))

        if start and end and end < start:
            raise serializers.ValidationError({
                "ended_at": "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."
            })
        return attrs

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_is_ongoing(self, obj):
        return obj.is_ongoing
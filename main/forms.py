from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, ClearableFileInput, DateInput

from main.models import Skill, Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "proficiency", "icon_slug"]

        labels = {
            "name": "Nama Skill",
            "category": "Kategori",
            "proficiency": "Tingkat Kemahiran",
            "icon_slug": "Slug Ikon (opsional)",
        }

        widgets = {
            "name": TextInput(
                attrs={"placeholder": "Masukkan skill di sini...", "maxlength": 100}
            ),
            "category": Select(),
            "proficiency": Select(),
            "icon_slug": TextInput(
                attrs={"placeholder": "python/python-original — cari di devicon.dev"}
            ),
        }

class ExperienceForm(ModelForm):
    started_at = forms.DateField(
        label="Bulan Mulai",
        input_formats=["%Y-%m"],
        widget=DateInput(attrs={"type": "month"}, format="%Y-%m"),
    )
    ended_at = forms.DateField(
        label="Bulan Selesai (kosongkan jika masih berjalan)",
        input_formats=["%Y-%m"],
        widget=DateInput(attrs={"type": "month"}, format="%Y-%m"),
        required=False,
    )
    class Meta:
        model = Experience
        fields = ["title", "organization", "description", "category", "started_at", "ended_at", "thumbnail", "image"]
        labels = {
            "title": "Judul",
            "organization": "Organisasi",
            "description": "Deskripsi (satu poin per baris)",
            "category": "Kategori",
            "started_at": "Bulan Mulai",
            "ended_at": "Bulan Selesai (kosongkan jika masih berjalan)",
            "thumbnail": "URL Thumbnail",
            "image": "Gambar",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Masukkan experience di sini...", "maxlength": 255}),
            "organization": TextInput(attrs={"placeholder": "Nama perusahaan/organisasi"}),
            "description": Textarea(attrs={"placeholder": "Satu bullet point per baris", "rows": 4}),
            "category": Select(),
            "thumbnail": URLInput(attrs={"placeholder": "https://..."}),
            "image": ClearableFileInput(),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama experience tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

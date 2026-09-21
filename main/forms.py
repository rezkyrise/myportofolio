from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, ClearableFileInput, DateInput

from main.models import Skill, Experience


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

from django.forms import ModelForm, TextInput, Select

from main.models import Skill


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "proficiency"]

        labels = {
            "name": "Nama Skill",
            "category": "Kategori",
            "proficiency": "Tingkat Kemahiran",
        }

        widgets = {
            "name": TextInput(
                attrs={"placeholder": "Python, Django, Git & GitHub, ...", "maxlength": 100}
            ),
            "category": Select(),
            "proficiency": Select(),
        }
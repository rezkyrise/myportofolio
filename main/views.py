from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Skill
from main.forms import SkillForm


def show_main(request):
    context = {
        "name": "M. Rezky Syahputra",
        "npm": "2506614006",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    experiences = Experience.objects.all().order_by('started_at')
    for experience in experiences:
        experience.bullet_points = [
            line.strip() for line in experience.description.split("\n") if line.strip()
        ]

    context = {
        "name": "M. Rezky Syahputra",
        "experience_list": experiences,
    }
    return render(request, "experience.html", context)

SKILL_ICON_MAP = {
    "python": "python/python-original",
    "java": "java/java-original",
    "c++": "cplusplus/cplusplus-original",
    "html5": "html5/html5-original",
    "css3": "css3/css3-original",
    "javascript": "javascript/javascript-original",
    "django": "django/django-plain",
    "git & github": "git/git-original",
    "vs code": "vscode/vscode-original",
    "sqlite & postgresql": "postgresql/postgresql-original",
    "latex": "latex/latex-original",
}


def show_skill(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    for skill in skills:
        slug = SKILL_ICON_MAP.get(skill.name.lower())
        if slug:
            skill.icon_url = f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{slug}.svg"
        else:
            skill.icon_url = None

    context = {
        "name": "M. Rezky Syahputra",
        "skill_list": skills,
        "name_query": name_query,
    }
    return render(request, "skill.html", context)


def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
    }
    return render(request, "skill_form.html", context)


def get_skill_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")


def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")
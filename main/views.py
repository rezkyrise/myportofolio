from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Skill
from main.forms import SkillForm, ExperienceForm


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
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experiences = [e.object for e in experiences]

    for experience in experiences:
        experience.bullet_points = [
            line.strip() for line in experience.description.split("\n") if line.strip()
        ]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "M. Rezky Syahputra",
        "experience_list": experiences,
        "title_query": title_query,
        "sort": request.GET.get("sort", "title_asc"),
    }
    return render(request, "experience.html", context)

def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skill")

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
        "skill": skill,
    }
    return render(request, "skill_form.html", context)


def show_skill(request):
    json_response = get_skill_json(request)
    skills = serializers.deserialize("json", json_response.content.decode("utf-8"))
    skills = [s.object for s in skills]

    for skill in skills:
        skill.icon_url = (
            f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{skill.icon_slug}.svg"
            if skill.icon_slug else None
        )

    context = {
        "name": "M. Rezky Syahputra",
        "skill_list": skills,
        "name_query": request.GET.get("name", "").strip(),
        "sort": request.GET.get("sort", "asc"),
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
    sort = request.GET.get("sort", "asc")
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    order_field = "name" if sort == "asc" else "-name"
    skills = skills.order_by(order_field)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")



def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

def create_experience(request):
    form = ExperienceForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, request.FILES or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    sort = request.GET.get("sort", "title_asc")
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    sort_map = {
        "title_asc": "title",
        "title_desc": "-title",
        "date_asc": "started_at",
        "date_desc": "-started_at",
    }

    experiences = experiences.order_by(sort_map.get(sort, "title"))

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

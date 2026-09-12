from django.shortcuts import render

from main.models import Experience, Skill


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
    context = {
        "name": "M. Rezky Syahputra",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = {
        "name": "M. Rezky Syahputra",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)
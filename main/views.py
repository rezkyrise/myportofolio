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
    experiences = Experience.objects.all()
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
    skills = Skill.objects.all()
    for skill in skills:
        slug = SKILL_ICON_MAP.get(skill.name.lower())
        if slug:
            skill.icon_url = f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{slug}.svg"
        else:
            skill.icon_url = None

    context = {
        "name": "M. Rezky Syahputra",
        "skill_list": skills,
    }
    return render(request, "skill.html", context)
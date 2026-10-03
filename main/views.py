from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Skill
from main.forms import SkillForm, ExperienceForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "M. Rezky Syahputra",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "M. Rezky Syahputra",
        "npm": "2506614006",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "M. Rezky Syahputra",
        'form': ExperienceForm(),
        "title_query": title_query,
        "sort": request.GET.get("sort", "title_asc"),
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
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
    context = {
        "name": "M. Rezky Syahputra",
        "name_query": request.GET.get("name", "").strip(),
        "sort": request.GET.get("sort", "asc"),
        "is_editor": is_editor(request.user),
        "form": SkillForm(),
    }
    return render(request, "skill.html", context)

@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
     
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
    skills = Skill.objects.prefetch_related('starred_by').all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    order_field = "name" if sort == "asc" else "-name"
    skills = skills.order_by(order_field)

    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "icon_slug": skill.icon_slug,
                "category": skill.category,
                "category_display": skill.get_category_display(),  # Menghasilkan label seperti 'Programming Language'
                "proficiency": skill.proficiency,
                "proficiency_display": skill.get_proficiency_display(),  # Menghasilkan label seperti 'Intermediate'
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    sort = request.GET.get("sort", "title_asc")
    
    # Gunakan prefetch_related agar query relasi starred_by lebih efisien
    experiences = Experience.objects.prefetch_related('starred_by').all()

    # Filter berdasarkan judul jika ada query
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Pemetaan opsi sorting
    sort_map = {
        "title_asc": "title",
        "title_desc": "-title",
        "date_asc": "started_at",
        "date_desc": "-started_at",
    }

    order_field = sort_map.get(sort, "title")
    experiences = experiences.order_by(order_field)

    data = []
    for exp in experiences:
        starred_users = exp.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "organization": exp.organization,
                "description": exp.description,
                "category": exp.category,
                "category_display": exp.get_category_display(),  # Label 'human-readable' dari choices
                "thumbnail": exp.thumbnail,
                "started_at": exp.started_at.isoformat() if exp.started_at else None,
                "ended_at": exp.ended_at.isoformat() if exp.ended_at else None,
                "is_ongoing": exp.is_ongoing,  # Memanfaatkan @property is_ongoing
                "image_url": exp.image.url if exp.image else None,  # URL file image jika diunggah
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def _toggle_star(request, obj):
    """Membalik status star user pada obj, lalu membalas JSON terbaru.

    Status: 200 berhasil, 401 jika belum login.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Silakan login untuk memberi star."}, status=401)

    if request.user in obj.starred_by.all():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)

    starred_users = obj.starred_by.all()
    return JsonResponse({
        "is_starred": request.user in starred_users,
        "star_count": starred_users.count(),
        "starred_by_names": ", ".join(u.username for u in starred_users),
    })


@require_POST
def toggle_star_skill(request, skill_id):
    return _toggle_star(request, get_object_or_404(Skill, pk=skill_id))


@require_POST
def toggle_star_experience(request, experience_id):
    return _toggle_star(request, get_object_or_404(Experience, pk=experience_id))

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST, request.FILES)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan skill."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Skill berhasil ditambahkan.", "pk": str(skill.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
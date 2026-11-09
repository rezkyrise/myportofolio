from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Skill
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly, IsSkillOwnerOrEditorOrReadOnly
from main.serializers import ExperienceSerializer, SkillSerializer


@api_view(["GET", "POST"])
@permission_classes([IsSkillOwnerOrEditorOrReadOnly])
def skill_list_create(request):
    if request.method == "GET":
        skills = Skill.objects.prefetch_related("starred_by").all()

        name_query = request.query_params.get("name", "").strip()
        if name_query:
            skills = skills.filter(name__icontains=name_query)

        sort = request.query_params.get("sort", "asc")
        skills = skills.order_by("-name" if sort == "desc" else "name")

        serializer = SkillSerializer(
            skills,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = SkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsSkillOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(
        Skill.objects.prefetch_related("starred_by"),
        pk=skill_id,
    )

    if request.method == "GET":
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = SkillSerializer(
            skill,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    skill.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    skill = get_object_or_404(
        Skill.objects.prefetch_related("starred_by"),
        pk=skill_id,
    )

    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)

    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)

@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list_create(request):
    if request.method == "GET":
        experiences = Experience.objects.prefetch_related("starred_by").all()

        title_query = request.query_params.get("title", "").strip()
        if title_query:
            experiences = experiences.filter(title__icontains=title_query)

        sort_map = {
            "title_asc": "title",
            "title_desc": "-title",
            "date_asc": "started_at",
            "date_desc": "-started_at",
        }
        sort = request.query_params.get("sort", "title_asc")
        experiences = experiences.order_by(sort_map.get(sort, "title"))

        serializer = ExperienceSerializer(
            experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=experience_id,
    )

    if request.method == "GET":
        serializer = ExperienceSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method in ("PUT", "PATCH"):
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=(request.method == "PATCH"),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    experience.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=experience_id,
    )

    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    serializer = ExperienceSerializer(
        experience,
        context={"request": request},
    )
    return Response(serializer.data)
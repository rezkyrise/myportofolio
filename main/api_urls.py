from django.urls import path

from main.api_views import skill_detail, skill_list_create, skill_star


app_name = "api"

urlpatterns = [
    path("skills/", skill_list_create, name="skill-list"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill-detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill-star"),
]
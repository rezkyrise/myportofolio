from django.urls import path

from main.api_views import experience_detail, experience_list_create, experience_star, skill_detail, skill_list_create, skill_star


app_name = "api"

urlpatterns = [
    path("skills/", skill_list_create, name="skill-list"),
    path("experiences/", experience_list_create, name="experience-list"),
    path("experiences/<uuid:experience_id>/", experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", experience_star, name="experience-star"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill-detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill-star"),
]
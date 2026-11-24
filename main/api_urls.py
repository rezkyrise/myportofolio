from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from main.api_views import api_logout
from main.api_views import experience_detail, experience_list_create, experience_star, skill_detail, skill_list_create, skill_star


app_name = "api"

urlpatterns = [
    path("skills/", skill_list_create, name="skill-list"),
    path("experiences/", experience_list_create, name="experience-list"),
    path("experiences/<uuid:experience_id>/", experience_detail, name="experience-detail"),
    path("experiences/<uuid:experience_id>/star/", experience_star, name="experience-star"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill-detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill-star"),
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_logout, name="api_logout"),
]
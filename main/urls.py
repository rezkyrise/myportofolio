from django.urls import path

from main.views import (
    show_main,
    show_experience, create_experience, update_experience, delete_experience, get_experience_json,
    show_skill, create_skill, update_skill, delete_skill, get_skill_json,
)


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("skill/", show_skill, name="show_skill"),
    path("skill/add/", create_skill, name="create_skill"),
    path("skill/<uuid:skill_id>/update/", update_skill, name="update_skill"),
    path("skill/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("api/skill/", get_skill_json, name="get_skill_json"),
]
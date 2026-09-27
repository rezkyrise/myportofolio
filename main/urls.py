from django.urls import path

from main.views import (
    show_main,
    show_experience, create_experience, update_experience, delete_experience, get_experience_json,
    show_skill, create_skill, update_skill, delete_skill, get_skill_json,
    register, login_user, logout_user,
    toggle_star_skill, toggle_star_experience,
)


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
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
    path("skill/<uuid:skill_id>/star/", toggle_star_skill, name="toggle_star_skill"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),
]
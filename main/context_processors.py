def user_role(request):
    """Sediakan `user_role` dan `name` ke semua template, termasuk halaman error 403."""
    user = request.user
    if not user.is_authenticated:
        role = None
    elif user.is_superuser:
        role = "Owner"
    elif user.groups.filter(name="Editor").exists():
        role = "Editor"
    else:
        role = "User"
    return {"user_role": role, "name": "M. Rezky Syahputra"}
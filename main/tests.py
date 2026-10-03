import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Skill

XSS_PAYLOAD = '<img src="x" onerror="alert(\'XSS!\')">'


class MainTest(TestCase):
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ExperienceTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=datetime.date(2026, 1, 1),
        )
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.regular = User.objects.create_user("biasa", password="pass12345")
        self.payload = {
            "title": "Magang Backend",
            "organization": "PT Contoh",
            "description": "Membangun API.",
            "category": "internship",
            "started_at": "2026-01",
        }

    # --- model dan halaman ---
    def test_model_ongoing_and_completed(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertTrue(self.experience.is_ongoing)
        self.experience.ended_at = datetime.date(2026, 6, 1)
        self.assertFalse(self.experience.is_ongoing)

    def test_page_renders_skeleton_only(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-list"')
        # Data dimuat lewat AJAX, jadi tidak ada di HTML awal
        self.assertNotContains(response, self.experience.title)

    # --- endpoint JSON ---
    def test_json_returns_experience_data(self):
        response = self.client.get(reverse("main:get_experience_json"))
        fields = response.json()[0]["fields"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(fields["title"], "Asisten Dosen PBP")
        self.assertEqual(fields["category_display"], "Part-Time")
        self.assertTrue(fields["is_ongoing"])
        self.assertEqual(fields["star_count"], 0)
        self.assertFalse(fields["is_starred"])

    def test_json_search_filters_by_title(self):
        url = reverse("main:get_experience_json")

        self.assertEqual(len(self.client.get(url, {"title": "dosen"}).json()), 1)
        self.assertEqual(self.client.get(url, {"title": "zzz"}).json(), [])

    def test_json_includes_star_info_for_logged_in_user(self):
        self.experience.starred_by.add(self.regular)
        self.client.login(username="biasa", password="pass12345")
        fields = self.client.get(reverse("main:get_experience_json")).json()[0]["fields"]

        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["star_count"], 1)
        self.assertEqual(fields["starred_by_names"], "biasa")

    # --- tambah data via AJAX ---
    def test_create_requires_post(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.get(reverse("main:create_experience_ajax"))

        self.assertEqual(response.status_code, 405)

    def test_create_forbidden_for_anonymous_and_regular_user(self):
        url = reverse("main:create_experience_ajax")

        self.assertEqual(self.client.post(url, self.payload).status_code, 403)
        self.client.login(username="biasa", password="pass12345")
        self.assertEqual(self.client.post(url, self.payload).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_create_success_for_superuser(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(reverse("main:create_experience_ajax"), self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)

    def test_create_rejects_xss_title(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            reverse("main:create_experience_ajax"), {**self.payload, "title": XSS_PAYLOAD}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertEqual(Experience.objects.count(), 1)

    def test_create_strips_html_tags(self):
        self.client.login(username="owner", password="pass12345")
        self.client.post(
            reverse("main:create_experience_ajax"),
            {**self.payload, "title": "<b>Halo</b> dunia", "organization": "<i>PT</i> X"},
        )
        created = Experience.objects.get(title="Halo dunia")

        self.assertEqual(created.organization, "PT X")

    def test_create_rejects_end_before_start(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            reverse("main:create_experience_ajax"),
            {**self.payload, "started_at": "2026-03", "ended_at": "2026-01"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("ended_at", response.json()["errors"])

    # --- star via AJAX ---
    def test_star_requires_login(self):
        url = reverse("main:toggle_star_experience", args=[self.experience.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_requires_post(self):
        self.client.login(username="biasa", password="pass12345")
        url = reverse("main:toggle_star_experience", args=[self.experience.id])

        self.assertEqual(self.client.get(url).status_code, 405)

    def test_star_toggles_on_and_off(self):
        self.client.login(username="biasa", password="pass12345")
        url = reverse("main:toggle_star_experience", args=[self.experience.id])

        first = self.client.post(url)
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.json()["is_starred"])
        self.assertEqual(first.json()["star_count"], 1)

        second = self.client.post(url)
        self.assertFalse(second.json()["is_starred"])
        self.assertEqual(second.json()["star_count"], 0)

    # --- hapus (masih versi redirect) ---
    def test_delete_forbidden_for_regular_user(self):
        self.client.login(username="biasa", password="pass12345")
        url = reverse("main:delete_experience", args=[self.experience.id])

        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)

    def test_delete_works_for_superuser(self):
        self.client.login(username="owner", password="pass12345")
        url = reverse("main:delete_experience", args=[self.experience.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 0)


class SkillTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python", category="language", proficiency="advanced"
        )
        self.owner = User.objects.create_superuser("owner", password="pass12345")
        self.regular = User.objects.create_user("biasa", password="pass12345")
        self.payload = {
            "name": "Django",
            "category": "framework",
            "proficiency": "intermediate",
        }

    # --- halaman dan JSON ---
    def test_page_renders_skeleton_only(self):
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, 'id="skill-grid"')
        self.assertNotContains(response, "Python")

    def test_json_returns_skill_data(self):
        response = self.client.get(reverse("main:get_skill_json"))
        fields = response.json()[0]["fields"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(fields["name"], "Python")
        self.assertEqual(fields["proficiency_display"], "Advanced")
        self.assertEqual(fields["star_count"], 0)

    def test_json_search_filters_by_name(self):
        url = reverse("main:get_skill_json")

        self.assertEqual(len(self.client.get(url, {"name": "pyth"}).json()), 1)
        self.assertEqual(self.client.get(url, {"name": "zzz"}).json(), [])

    # --- tambah data via AJAX ---
    def test_create_forbidden_for_anonymous_and_regular_user(self):
        url = reverse("main:create_skill_ajax")

        self.assertEqual(self.client.post(url, self.payload).status_code, 403)
        self.client.login(username="biasa", password="pass12345")
        self.assertEqual(self.client.post(url, self.payload).status_code, 403)
        self.assertEqual(Skill.objects.count(), 1)

    def test_create_success_for_superuser(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(reverse("main:create_skill_ajax"), self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Skill.objects.count(), 2)

    def test_create_rejects_xss_name(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            reverse("main:create_skill_ajax"), {**self.payload, "name": XSS_PAYLOAD}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json()["errors"])

    def test_create_rejects_invalid_icon_slug(self):
        self.client.login(username="owner", password="pass12345")
        response = self.client.post(
            reverse("main:create_skill_ajax"), {**self.payload, "icon_slug": "../x"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("icon_slug", response.json()["errors"])

    # --- star via AJAX ---
    def test_star_requires_login(self):
        url = reverse("main:toggle_star_skill", args=[self.skill.id])

        self.assertEqual(self.client.post(url).status_code, 401)
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_star_toggles_on_and_off(self):
        self.client.login(username="biasa", password="pass12345")
        url = reverse("main:toggle_star_skill", args=[self.skill.id])

        first = self.client.post(url)
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.json()["is_starred"])
        self.assertEqual(first.json()["star_count"], 1)

        second = self.client.post(url)
        self.assertFalse(second.json()["is_starred"])
        self.assertEqual(second.json()["star_count"], 0)

    # --- hapus (masih versi redirect) ---
    def test_delete_forbidden_for_regular_user(self):
        self.client.login(username="biasa", password="pass12345")
        url = reverse("main:delete_skill", args=[self.skill.id])

        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertEqual(Skill.objects.count(), 1)

    def test_delete_works_for_superuser(self):
        self.client.login(username="owner", password="pass12345")
        url = reverse("main:delete_skill", args=[self.skill.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Skill.objects.count(), 0)
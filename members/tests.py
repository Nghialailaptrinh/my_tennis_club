from django.test import TestCase

from django.db.models.deletion import ProtectedError
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import ClassRoom, Member, Teacher


class ClassDirectoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(firstname="An", lastname="Nguyen")
        cls.member = Member.objects.create(firstname="Binh", lastname="Tran", slug="binh-tran")
        cls.classroom = ClassRoom.objects.create(name="Beginner tennis", teacher=cls.teacher)
        cls.classroom.members.add(cls.member)

    def test_class_links_to_teacher_and_enrolled_members_only(self):
        Member.objects.create(firstname="Other", lastname="Member", slug="other-member")
        response = self.client.get(reverse("class_details", args=[self.classroom.pk]))
        self.assertContains(response, reverse("teacher_details", args=[self.teacher.pk]))
        self.assertContains(response, reverse("details", args=[self.member.slug]))
        self.assertNotContains(response, "Other Member")

    def test_directory_and_teacher_links(self):
        class_url = reverse("class_details", args=[self.classroom.pk])
        self.assertContains(self.client.get(reverse("classes")), class_url)
        self.assertContains(self.client.get(reverse("teachers")), str(self.teacher))
        self.assertContains(self.client.get(reverse("teacher_details", args=[self.teacher.pk])), class_url)

    def test_missing_records_return_404(self):
        for name in ("class_details", "teacher_details"):
            self.assertEqual(self.client.get(reverse(name, args=[999])).status_code, 404)

    def test_empty_states(self):
        self.classroom.members.clear()
        self.assertContains(self.client.get(reverse("class_details", args=[self.classroom.pk])), "There are no members")
        self.classroom.delete()
        self.assertContains(self.client.get(reverse("classes")), "There are no classes")
        self.teacher.delete()
        self.assertContains(self.client.get(reverse("teachers")), "There are no teachers")
        self.assertContains(self.client.get(reverse("library")), "The library is empty")

    def test_teacher_in_use_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.teacher.delete()

    def test_admin_creates_and_updates_class_with_existing_members_without_teacher(self):
        admin = get_user_model().objects.create_superuser(
            username="class-admin", password="test-password"
        )
        self.client.force_login(admin)
        second = Member.objects.create(firstname="Chi", lastname="Le", slug="chi-le")
        add_url = reverse("admin:members_classroom_add")
        response = self.client.get(add_url)
        self.assertContains(response, str(self.member))
        self.assertContains(response, str(second))
        response = self.client.post(add_url, {
            "name": "Evening class", "teacher": "",
            "members": [self.member.pk, second.pk], "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        classroom = ClassRoom.objects.get(name="Evening class")
        self.assertIsNone(classroom.teacher)
        self.assertSetEqual(set(classroom.members.all()), {self.member, second})
        self.assertEqual(self.member.classes.count(), 2)
        self.assertContains(self.client.get(reverse("classes")), "Evening class")
        detail_url = reverse("class_details", args=[classroom.pk])
        self.assertContains(self.client.get(detail_url), str(second))

        response = self.client.post(reverse("admin:members_classroom_change", args=[classroom.pk]), {
            "name": classroom.name, "teacher": "", "members": [second.pk], "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        self.assertSetEqual(set(classroom.members.all()), {second})
        self.assertTrue(Member.objects.filter(pk=self.member.pk).exists())
        self.assertTrue(self.classroom.members.filter(pk=self.member.pk).exists())

from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)
  slug = models.SlugField(default="", null=False)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"


class Teacher(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.CharField(max_length=30, blank=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"


class ClassRoom(models.Model):
  name = models.CharField(max_length=255)
  teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="classes", null=True, blank=True)
  members = models.ManyToManyField(Member, blank=True, related_name="classes")

  class Meta:
    verbose_name = "class"
    verbose_name_plural = "classes"

  def __str__(self):
    return self.name

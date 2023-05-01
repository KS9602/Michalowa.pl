from django.db import models
from django.contrib.auth.models import User


class ForumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)

    user_pictrue = models.ImageField(
        default="images/users/default.jpg",
        upload_to="images/users",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nick


class Section(models.Model):
    name = models.CharField(max_length=30)
    section_description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=50)
    subject_description = models.TextField(max_length=3000)
    date_created = models.DateField(auto_now_add=True)

    subject_pictrue = models.ImageField(
        default="images/subject_pic/kotki.png",
        upload_to="images/subject_pic",
        null=True,
        blank=True,
    )

    subject_creator = models.ForeignKey(
        ForumUser, on_delete=models.CASCADE, related_name="subject", null=True
    )
    subject_section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="subject", null=True
    )
    likes = models.ManyToManyField(ForumUser, related_name="liked_subjects")

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField(max_length=3000)
    date_created = models.DateField(auto_now_add=True)

    subject_pictrue = models.ImageField(
        default="images/subject_pic/kotki.png",
        upload_to="images/subject_pic",
        null=True,
        blank=True,
    )

    topic = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="post", null=True
    )
    post_creator = models.ForeignKey(
        ForumUser, on_delete=models.CASCADE, related_name="post", null=True
    )

    def __str__(self):
        return f"{self.date_created}"

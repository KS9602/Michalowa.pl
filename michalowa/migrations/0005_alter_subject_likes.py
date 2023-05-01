# Generated by Django 4.1.7 on 2023-05-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("michalowa", "0004_remove_subject_likes_subject_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="likes",
            field=models.ManyToManyField(
                related_name="liked_subjects", to="michalowa.forumuser"
            ),
        ),
    ]
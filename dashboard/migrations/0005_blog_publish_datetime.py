# Generated by Django 4.0.5 on 2022-06-12 03:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_blog_content_alter_blog_image_path_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publish_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

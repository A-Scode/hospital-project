# Generated by Django 4.0.5 on 2022-06-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_remove_blog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content',
            field=models.TextField(null=True),
        ),
    ]

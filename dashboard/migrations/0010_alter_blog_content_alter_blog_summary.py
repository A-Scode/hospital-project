# Generated by Django 4.0.5 on 2022-06-12 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_blog_content_alter_blog_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.CharField(max_length=300, null=True),
        ),
    ]

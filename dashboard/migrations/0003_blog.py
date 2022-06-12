# Generated by Django 4.0.5 on 2022-06-11 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_user_user_status_alter_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('blog_title', models.CharField(max_length=50)),
                ('image_path', models.CharField(default='', max_length=500)),
                ('category', models.CharField(choices=[('Metal Helth', 'Metal Helth'), ('Heart Disease', 'Heart Disease'), ('COVID-19', 'COVID-19'), ('Immunization', 'Immunization')], max_length=100)),
                ('summary', models.CharField(default='No Summary', max_length=300)),
                ('content', models.CharField(default='No Content', max_length=2000)),
                ('blog_status', models.CharField(choices=[('Draft', 'Draft'), ('Uploaded', 'Uploaded')], max_length=50)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.user')),
            ],
        ),
    ]
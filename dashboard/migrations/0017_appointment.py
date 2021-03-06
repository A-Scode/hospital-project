# Generated by Django 4.0.5 on 2022-06-14 10:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_remove_blog_text_blog_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=50)),
                ('req_speciality', models.TextField(default='', max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.doctor')),
                ('paitient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paitient')),
            ],
        ),
    ]

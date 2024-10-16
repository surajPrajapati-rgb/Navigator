# Generated by Django 5.0.4 on 2024-10-08 20:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('mentor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='mentor_photos/')),
                ('graduation_year', models.IntegerField(blank=True, null=True)),
                ('field_of_study', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=100)),
                ('academic_stream', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True, null=True)),
                ('preferred_mentee_year', models.CharField(blank=True, max_length=50, null=True)),
                ('mentoring_frequency', models.CharField(blank=True, max_length=50, null=True)),
                ('session_duration', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_mode', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expertise_areas', to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('field', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_name', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('start_year', models.IntegerField()),
                ('end_year', models.IntegerField(blank=True, null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_slots', to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateTimeField()),
                ('duration', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='user_profiles.profile')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='mentorship.mentor')),
            ],
        ),
    ]

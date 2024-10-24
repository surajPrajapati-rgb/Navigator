
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('mentor_id', models.AutoField(primary_key=True, serialize=False)),
                ('bio', models.TextField(default='No bio provided')),
                ('experience_years', models.IntegerField(default=0)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('industry', models.CharField(max_length=100)),
                ('linkedin_url', models.URLField(blank=True, max_length=255, null=True)),
                ('education', models.CharField(default='Not specified', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MentorAvailability',
            fields=[
                ('availability_id', models.AutoField(primary_key=True, serialize=False)),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=9)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorCategory',
            fields=[
                ('mentor_category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default=1, max_length=100)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorSkill',
            fields=[
                ('mentor_skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorcategory')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.IntegerField()),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('title_review', models.CharField(max_length=100)),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_id', models.IntegerField()),
                ('session_topic', models.CharField(max_length=255)),
                ('session_duration', models.IntegerField()),
                ('session_notes', models.TextField()),
                ('session_date', models.DateTimeField()),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_sessions', to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=10)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.session')),
            ],
        ),
    ]

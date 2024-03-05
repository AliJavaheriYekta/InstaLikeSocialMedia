# Generated by Django 5.0.2 on 2024-03-01 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('avatar', models.ImageField(default='default.jpg', upload_to='profile_pics/')),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=265, unique=True),
        ),
    ]
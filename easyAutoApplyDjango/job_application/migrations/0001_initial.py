# Generated by Django 4.2.4 on 2023-10-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='jobApplication',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('owner_id', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('job_location', models.CharField(max_length=255)),
                ('resume', models.URLField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('created_date', models.CharField(max_length=255)),
                ('updated_date', models.CharField(max_length=255)),
                ('field_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='jobPlatformCred',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('owner_id', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_date', models.CharField(max_length=255)),
                ('updated_date', models.CharField(max_length=255)),
                ('field_id', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('cookies', models.CharField(max_length=255)),
            ],
        ),
    ]

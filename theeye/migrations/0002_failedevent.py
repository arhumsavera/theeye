# Generated by Django 3.2.8 on 2021-10-21 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theeye', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField()),
                ('error', models.JSONField()),
                ('received', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
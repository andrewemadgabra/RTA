# Generated by Django 3.2 on 2022-03-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('job_id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title_Ar', models.CharField(max_length=128, unique=True)),
                ('job_title_En', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'db_table': 'Jobs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserJobs',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('user_job_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'UserJobs',
                'managed': False,
            },
        ),
    ]

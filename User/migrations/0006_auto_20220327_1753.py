# Generated by Django 3.2 on 2022-03-27 15:53

import HelperClasses.DjangoValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20220324_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEmploymentJobStatus',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('user_employment_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'UserEmploymentJobStatus',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=14, unique=True, validators=[HelperClasses.DjangoValidator.DjangoValidator.validation_EgyptionMobileNumber]),
        ),
        migrations.AlterField(
            model_name='user',
            name='number_of_identification',
            field=models.CharField(db_column='number_of_identification', max_length=14, unique=True, validators=[HelperClasses.DjangoValidator.DjangoValidator.validation_numberOfIdentintification]),
        ),
        migrations.AlterModelTable(
            name='system',
            table='System_Table',
        ),
    ]